from datetime import timedelta
from decimal import Decimal
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.core.management import call_command
from pathlib import Path
from django.urls import reverse
from django.utils import timezone
from .models import Exercise, ExerciseFavorite, MuscleGroup, Workout, WorkoutExercise, WorkoutSet, UserPreference
from .services import transition_workout, InvalidWorkoutState

User = get_user_model()

class TrackerTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='athlete-one', password='StrongPass123!')
        self.group = MuscleGroup.objects.create(name='Chest', slug='chest')
        self.exercise = Exercise.objects.create(name='Dumbbell chest press', primary_muscle_group=self.group, description='Press.')
        self.workout = Workout.objects.create(title='Push day', user=self.user)
        self.workout.muscle_groups.add(self.group)
        self.entry = WorkoutExercise.objects.create(workout=self.workout, exercise=self.exercise)

    def test_seed_command_maps_matching_local_exercise_photos(self):
        call_command('seed_exercises')
        self.exercise.refresh_from_db()
        self.assertEqual(self.exercise.image, 'exercises/dumbbell-chest-press.jpeg')
        self.assertTrue((Path('static/tracker/images') / self.exercise.image).is_file())
        client = Client(); client.force_login(self.user)
        response = client.get(reverse('exercises'))
        self.assertContains(response, 'exercises/dumbbell-chest-press.jpeg')

    def test_exercise_and_muscle_group(self):
        self.assertEqual(str(self.exercise.primary_muscle_group), 'Chest')
        self.assertEqual(Exercise.objects.count(), 1)

    def test_workout_set_completion_and_volume(self):
        item = WorkoutSet.objects.create(workout_exercise=self.entry, set_number=1, repetitions=8, weight=Decimal('20'), is_completed=True, completed_at=timezone.now())
        self.assertEqual(self.workout.volume, Decimal('160'))
        self.assertEqual(item.volume, Decimal('160'))

    def test_pause_resume_and_elapsed_time(self):
        self.workout.started_at = timezone.now() - timedelta(minutes=10)
        self.workout.save()
        transition_workout(self.workout, 'pause')
        paused = Workout.objects.get(pk=self.workout.pk)
        self.assertEqual(paused.status, 'paused')
        before = paused.elapsed_seconds
        transition_workout(paused, 'resume')
        resumed = Workout.objects.get(pk=self.workout.pk)
        self.assertEqual(resumed.status, 'active')
        self.assertGreaterEqual(resumed.accumulated_paused_seconds, 0)
        self.assertGreaterEqual(resumed.elapsed_seconds, before)

    def test_finish_workout_state_transition(self):
        result = transition_workout(self.workout, 'finish')
        self.assertEqual(result.status, 'completed')
        self.assertIsNotNone(result.ended_at)
        with self.assertRaises(InvalidWorkoutState):
            transition_workout(result, 'pause')

    def test_authenticated_pages_render_for_owner(self):
        self.workout.status = 'completed'; self.workout.ended_at = timezone.now(); self.workout.save()
        client = Client()
        client.force_login(self.user)
        self.assertEqual(client.get(reverse('home')).status_code, 200)
        self.assertEqual(client.get(reverse('start_workout')).status_code, 200)
        self.assertEqual(client.get(reverse('workout')).status_code, 200)
        self.assertEqual(client.get(reverse('exercises')).status_code, 200)
        self.assertEqual(client.get(reverse('history')).status_code, 200)
        self.assertEqual(client.get(reverse('analytics')).status_code, 200)
        self.assertEqual(client.get(reverse('settings')).status_code, 200)

    def test_workout_flow_and_invalid_set(self):
        self.workout.status = 'completed'; self.workout.ended_at = timezone.now(); self.workout.save()
        client = Client()
        client.force_login(self.user)
        start = client.post(reverse('start_workout'), {'title': 'Leg day', 'muscle_groups': [self.group.pk]})
        self.assertEqual(start.status_code, 302)
        current = Workout.objects.get(user=self.user, status='active')
        self.assertContains(client.get(reverse('workout')), 'tracker/audio/can-we-get-much-higher-one-piece-meme.mp3')
        response = client.post(reverse('workout'), {'action':'add_exercise', 'exercise_id': self.exercise.pk})
        self.assertEqual(response.status_code, 302)
        entry = WorkoutExercise.objects.get(workout=current)
        response = client.post(reverse('workout'), {'action':'add_set', 'entry_id':entry.pk, 'set_number':1, 'repetitions':-2, 'weight':10})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(WorkoutSet.objects.count(), 0)
        client.post(reverse('workout'), {'action':'add_set', 'entry_id':entry.pk, 'set_number':1, 'repetitions':8, 'weight':10})
        self.assertEqual(WorkoutSet.objects.count(), 1)

    def test_completed_workout_detail_history_and_analytics(self):
        self.workout.status = 'completed'
        self.workout.ended_at = timezone.now()
        self.workout.save()
        WorkoutSet.objects.create(workout_exercise=self.entry, set_number=1, repetitions=10, weight=Decimal('12.5'), is_completed=True, completed_at=timezone.now())
        client = Client()
        client.force_login(self.user)
        self.assertEqual(client.get(reverse('workout_detail', args=[self.workout.pk])).status_code, 200)
        self.assertEqual(client.get(reverse('history')).status_code, 200)
        self.assertEqual(client.get(reverse('analytics')).status_code, 200)

    def test_registration_login_logout_use_hashed_passwords(self):
        client = Client()
        response = client.post(reverse('register'), {'username':'new-athlete', 'password1':'AnotherStrong123!', 'password2':'AnotherStrong123!'})
        self.assertEqual(response.status_code, 302)
        created = User.objects.get(username='new-athlete')
        self.assertNotEqual(created.password, 'AnotherStrong123!')
        self.assertTrue(created.check_password('AnotherStrong123!'))
        client.post(reverse('logout'))
        response = client.post(reverse('login'), {'username':'new-athlete', 'password':'AnotherStrong123!'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue('_auth_user_id' in client.session)
        client.post(reverse('logout'))
        self.assertNotIn('_auth_user_id', client.session)

    def test_private_pages_redirect_anonymous_users(self):
        client = Client()
        urls = ['home', 'start_workout', 'workout', 'exercises', 'history', 'analytics', 'settings']
        for name in urls:
            response = client.get(reverse(name))
            self.assertEqual(response.status_code, 302, name)
            self.assertIn(reverse('login'), response.url)
        self.assertEqual(client.get(reverse('register')).status_code, 200)
        self.assertEqual(client.get(reverse('login')).status_code, 200)
        self.assertEqual(client.post(reverse('logout')).status_code, 302)

    def test_workout_and_favorite_data_are_isolated_between_users(self):
        other = User.objects.create_user(username='athlete-two', password='OtherPass123!')
        self.workout.status = 'completed'
        self.workout.ended_at = timezone.now()
        self.workout.save()
        ExerciseFavorite.objects.create(user=self.user, exercise=self.exercise)
        client = Client()
        client.force_login(other)
        history_response = client.get(reverse('history'))
        self.assertNotContains(history_response, 'Push day')
        dashboard = client.get(reverse('home'))
        analytics = client.get(reverse('analytics'))
        self.assertEqual(dashboard.context['total_workouts'], 0)
        self.assertEqual(analytics.context['workout_count'], 0)
        self.assertEqual(client.get(reverse('workout_detail', args=[self.workout.pk])).status_code, 404)
        self.assertEqual(client.post(reverse('delete_workout', args=[self.workout.pk])).status_code, 404)
        exercises_response = client.get(reverse('exercises'))
        self.assertNotIn(self.exercise.pk, exercises_response.context['favorite_ids'])

    def test_legacy_owner_command_assigns_only_orphaned_rows(self):
        orphan = Workout.objects.create(title='Legacy workout')
        legacy_pref = UserPreference.objects.create(weight_unit='lb')
        call_command('assign_legacy_owner', username=self.user.username, stdout=None)
        orphan.refresh_from_db(); legacy_pref.refresh_from_db()
        self.assertEqual(orphan.user, self.user)
        self.assertEqual(legacy_pref.user, self.user)

    def test_preferences_are_per_user(self):
        other = User.objects.create_user(username='athlete-three', password='ThirdPass123!')
        pref = UserPreference.current(self.user)
        pref.weight_unit = 'lb'; pref.save()
        self.assertEqual(UserPreference.current(self.user).weight_unit, 'lb')
        self.assertEqual(UserPreference.current(other).weight_unit, 'kg')

    def test_workout_data_creation_uses_logged_in_user(self):
        self.workout.status = 'completed'; self.workout.ended_at = timezone.now(); self.workout.save()
        client = Client()
        client.force_login(self.user)
        response = client.post(reverse('start_workout'), {'title':'Pull day', 'muscle_groups':[self.group.pk]})
        self.assertEqual(response.status_code, 302)
        created = Workout.objects.get(title='Pull day')
        self.assertEqual(created.user, self.user)
