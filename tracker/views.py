from datetime import date, timedelta
from django.contrib import messages
from django.contrib.auth import login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count, Sum, Max, F, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST
from .forms import WorkoutStartForm, ExerciseFilterForm, SetForm, PreferenceForm, RegisterForm
from .models import Exercise, ExerciseFavorite, MuscleGroup, Workout, WorkoutExercise, WorkoutSet, UserPreference
from .services import transition_workout, InvalidWorkoutState


@login_required
@require_POST
def logout_user(request):
    auth_logout(request)
    return redirect('login')


def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, 'Your account is ready.')
        return redirect('home')
    return render(request, 'registration/register.html', {'form': form})


@login_required
def home(request):
    completed = Workout.objects.filter(user=request.user, status='completed')
    today = timezone.localdate()
    week_start = today - timedelta(days=today.weekday())
    week_count = completed.filter(ended_at__date__gte=week_start).count()
    total_seconds = sum(w.elapsed_seconds for w in completed)
    workout_dates = set(completed.values_list('ended_at__date', flat=True))
    streak, day = 0, today
    while day in workout_dates:
        streak += 1
        day -= timedelta(days=1)
    recent = completed.prefetch_related('workout_exercises__exercise').all()[:4]
    favs = Exercise.objects.filter(favorites__user=request.user)[:4]
    context = {
        'total_workouts': completed.count(), 'total_hours': total_seconds // 3600,
        'streak': streak, 'week_count': week_count, 'recent': recent, 'favorites': favs,
        'weekly_target': 4,
    }
    return render(request, 'tracker/home.html', context)


@login_required
def start_workout(request):
    if Workout.objects.filter(user=request.user, status__in=['active', 'paused']).exists():
        messages.info(request, 'You already have a workout in progress.')
        return redirect('workout')
    if request.method == 'POST':
        form = WorkoutStartForm(request.POST)
        if form.is_valid():
            workout = form.save(commit=False)
            workout.user = request.user
            workout.save()
            form.save_m2m()
            messages.success(request, 'Your workout is ready. Let’s get to work.')
            return redirect('workout')
    else:
        form = WorkoutStartForm()
    return render(request, 'tracker/start_workout.html', {'form': form})


@login_required
def workout_page(request):
    workout = Workout.objects.filter(user=request.user, status__in=['active', 'paused']).first()
    if not workout:
        return render(request, 'tracker/workout.html', {'workout': None})
    items = workout.workout_exercises.select_related('exercise').prefetch_related('sets')
    groups = workout.muscle_groups.all()
    exercises = Exercise.objects.select_related('primary_muscle_group').filter(Q(primary_muscle_group__in=groups) | Q(secondary_muscle_groups__in=groups)).distinct()
    if request.method == 'POST':
        action = request.POST.get('action')
        try:
            if action == 'add_exercise':
                exercise = get_object_or_404(Exercise, pk=request.POST.get('exercise_id'))
                if workout.muscle_groups.exists() and not (workout.muscle_groups.filter(pk=exercise.primary_muscle_group_id).exists() or exercise.secondary_muscle_groups.filter(pk__in=workout.muscle_groups.values('pk')).exists()):
                    messages.error(request, 'Choose an exercise that matches one of this workout’s muscle groups.')
                    return redirect('workout')
                WorkoutExercise.objects.get_or_create(workout=workout, exercise=exercise, defaults={'order': items.count()})
                messages.success(request, f'{exercise.name} added.')
            elif action == 'add_set':
                entry = get_object_or_404(WorkoutExercise, pk=request.POST.get('entry_id'), workout=workout)
                form = SetForm(request.POST)
                if form.is_valid() and not entry.sets.filter(set_number=form.cleaned_data['set_number']).exists():
                    obj = form.save(commit=False); obj.workout_exercise = entry; obj.save()
                    messages.success(request, 'Set added.')
                else:
                    messages.error(request, 'Check the set number, reps, and weight. Set numbers must be unique for each exercise.')
            elif action == 'toggle_set':
                workout_set = get_object_or_404(WorkoutSet, pk=request.POST.get('set_id'), workout_exercise__workout=workout)
                workout_set.is_completed = not workout_set.is_completed
                workout_set.completed_at = timezone.now() if workout_set.is_completed else None
                workout_set.save(update_fields=['is_completed', 'completed_at'])
            elif action == 'notes':
                workout.notes = request.POST.get('notes', '')[:5000]; workout.save(update_fields=['notes'])
                messages.success(request, 'Workout notes saved.')
            elif action in ('pause', 'resume', 'finish', 'cancel'):
                transition_workout(workout, action)
                if action == 'finish':
                    messages.success(request, 'Workout completed. Great work.')
                    return redirect('workout_detail', pk=workout.pk)
                if action == 'cancel':
                    messages.info(request, 'Workout cancelled.')
                    return redirect('home')
                messages.success(request, 'Workout ' + ('paused.' if action == 'pause' else 'resumed.'))
        except InvalidWorkoutState as exc:
            messages.error(request, str(exc))
        return redirect('workout')
    return render(request, 'tracker/workout.html', {'workout': workout, 'items': items, 'exercises': exercises, 'form': SetForm()})

@login_required
@require_POST
def timer_action(request, pk):
    workout = get_object_or_404(Workout, pk=pk, user=request.user)
    try:
        workout = transition_workout(workout, request.POST.get('action'))
    except InvalidWorkoutState as exc:
        return JsonResponse({'error': str(exc)}, status=400)
    return JsonResponse({'status': workout.status, 'elapsed': workout.elapsed_seconds})


@login_required
def exercises(request):
    form = ExerciseFilterForm(request.GET)
    qs = Exercise.objects.select_related('primary_muscle_group').prefetch_related('secondary_muscle_groups')
    q = request.GET.get('q', '').strip()
    muscle, equipment, difficulty = request.GET.get('muscle', ''), request.GET.get('equipment', ''), request.GET.get('difficulty', '')
    if q: qs = qs.filter(Q(name__icontains=q) | Q(description__icontains=q) | Q(equipment__icontains=q))
    if muscle: qs = qs.filter(Q(primary_muscle_group__slug=muscle) | Q(secondary_muscle_groups__slug=muscle)).distinct()
    if equipment: qs = qs.filter(equipment__icontains=equipment)
    if difficulty: qs = qs.filter(difficulty=difficulty)
    return render(request, 'tracker/exercises.html', {'exercises': qs, 'form': form, 'muscles': MuscleGroup.objects.all(), 'equipment_options': Exercise.objects.values_list('equipment', flat=True).distinct(), 'favorite_ids': set(ExerciseFavorite.objects.filter(user=request.user).values_list('exercise_id', flat=True))})


@login_required
@require_POST
def toggle_favorite(request, pk):
    exercise = get_object_or_404(Exercise, pk=pk)
    favorite, created = ExerciseFavorite.objects.get_or_create(user=request.user, exercise=exercise)
    if not created:
        favorite.delete()
    return redirect('exercises')


@login_required
def history(request):
    qs = Workout.objects.filter(user=request.user, status='completed').prefetch_related('workout_exercises__exercise__primary_muscle_group', 'workout_exercises__sets')
    start, end, muscle = request.GET.get('start', ''), request.GET.get('end', ''), request.GET.get('muscle', '')
    try:
        if start: date.fromisoformat(start); qs = qs.filter(ended_at__date__gte=start)
        if end: date.fromisoformat(end); qs = qs.filter(ended_at__date__lte=end)
    except ValueError:
        start, end = '', ''
        messages.error(request, 'Enter dates in a valid calendar format.')
    if muscle: qs = qs.filter(Q(workout_exercises__exercise__primary_muscle_group__slug=muscle) | Q(workout_exercises__exercise__secondary_muscle_groups__slug=muscle) | Q(muscle_groups__slug=muscle)).distinct()
    return render(request, 'tracker/history.html', {'workouts': qs, 'muscles': MuscleGroup.objects.all(), 'filters': request.GET})


@login_required
def workout_detail(request, pk):
    workout = get_object_or_404(Workout, pk=pk, user=request.user, status='completed')
    items = workout.workout_exercises.select_related('exercise__primary_muscle_group').prefetch_related('sets')
    total_sets = WorkoutSet.objects.filter(workout_exercise__workout=workout, is_completed=True).count()
    total_reps = WorkoutSet.objects.filter(workout_exercise__workout=workout, is_completed=True).aggregate(v=Sum('repetitions'))['v'] or 0
    return render(request, 'tracker/workout_detail.html', {'workout': workout, 'items': items, 'total_sets': total_sets, 'total_reps': total_reps})

@login_required
@require_POST
def delete_workout(request, pk):
    workout = get_object_or_404(Workout, pk=pk, user=request.user, status__in=['completed', 'cancelled'])
    workout.delete(); messages.success(request, 'Workout history deleted.')
    return redirect('history')


@login_required
def analytics(request):
    completed = Workout.objects.filter(user=request.user, status='completed')
    today = timezone.localdate()
    days = [today - timedelta(days=6-i) for i in range(7)]
    daily = []
    for day in days:
        qs = WorkoutSet.objects.filter(workout_exercise__workout__user=request.user, is_completed=True, completed_at__date=day)
        daily.append({'label': day.strftime('%a'), 'sets': qs.count(), 'volume': float(qs.aggregate(v=Sum(F('weight')*F('repetitions')))['v'] or 0), 'workouts': completed.filter(ended_at__date=day).count(), 'minutes': sum(w.elapsed_seconds for w in completed.filter(ended_at__date=day)) // 60})
    distribution = list(WorkoutExercise.objects.filter(workout__user=request.user, workout__status='completed').values('exercise__primary_muscle_group__name').annotate(total=Count('id')).order_by('-total')[:8])
    progression = list(WorkoutSet.objects.filter(is_completed=True, workout_exercise__workout__user=request.user, workout_exercise__workout__status='completed').values('workout_exercise__exercise__name').annotate(volume=Sum(F('weight')*F('repetitions'))).order_by('-volume')[:5])
    recent_sets = WorkoutSet.objects.filter(is_completed=True, workout_exercise__workout__user=request.user, workout_exercise__workout__status='completed').values('workout_exercise__exercise__name', 'workout_exercise__workout__ended_at').annotate(best_weight=Max('weight')).order_by('-workout_exercise__workout__ended_at')
    exercise_progression = {}
    for row in recent_sets:
        name = row['workout_exercise__exercise__name']
        exercise_progression.setdefault(name, []).append({'date': row['workout_exercise__workout__ended_at'], 'weight': row['best_weight']})
    exercise_progression = [{'name': name, 'records': records[:5]} for name, records in list(exercise_progression.items())[:4]]
    return render(request, 'tracker/analytics.html', {'days': daily, 'distribution': distribution, 'progression': progression, 'exercise_progression': exercise_progression, 'workout_count': completed.count(), 'total_sets': WorkoutSet.objects.filter(is_completed=True, workout_exercise__workout__user=request.user, workout_exercise__workout__status='completed').count(), 'total_volume': sum(float(w.volume) for w in completed)})


@login_required
def settings_page(request):
    prefs = UserPreference.current(request.user)
    if request.method == 'POST':
        form = PreferenceForm(request.POST, instance=prefs)
        if form.is_valid(): form.save(); messages.success(request, 'Preferences updated.'); return redirect('settings')
    else: form = PreferenceForm(instance=prefs)
    return render(request, 'tracker/settings.html', {'form': form, 'prefs': prefs})
