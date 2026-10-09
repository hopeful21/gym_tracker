from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from tracker.models import UserPreference, Workout

class Command(BaseCommand):
    help = 'Assign legacy ownerless workouts and preferences to an explicitly chosen username.'

    def add_arguments(self, parser):
        parser.add_argument('--username', required=True, help='Existing account that should own the legacy records.')

    @transaction.atomic
    def handle(self, *args, **options):
        User = get_user_model()
        try:
            user = User.objects.get(username=options['username'])
        except User.DoesNotExist as exc:
            raise CommandError(f"No user named {options['username']!r}. Create or choose an account first.") from exc
        workouts = Workout.objects.filter(user__isnull=True).update(user=user)
        preferences = UserPreference.objects.filter(user__isnull=True)
        preference_count = 0
        if preferences.exists() and not UserPreference.objects.filter(user=user).exists():
            preference_count = preferences.update(user=user)
        self.stdout.write(self.style.SUCCESS(
            f'Assigned {workouts} legacy workout(s) and {preference_count} preference row(s) to {user.username}.'
        ))
        if preferences.exists() and not preference_count:
            self.stdout.write(self.style.WARNING(
                'An unowned preference row remains because this account already has preferences; it was preserved.'
            ))
