from django.utils import timezone
from .models import Workout, WorkoutSet, UserPreference

def site_state(request):
    if not request.user.is_authenticated:
        return {'site_workout': None, 'today_completed_sets': 0, 'preferences': None}
    workout = Workout.objects.filter(user=request.user, status__in=['active', 'paused']).first()
    today_sets = WorkoutSet.objects.filter(workout_exercise__workout__user=request.user, is_completed=True, completed_at__date=timezone.localdate()).count()
    preferences = UserPreference.objects.filter(user=request.user).first()
    return {'site_workout': workout, 'today_completed_sets': today_sets, 'preferences': preferences}
