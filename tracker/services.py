from django.db import transaction
from django.utils import timezone
from .models import Workout


class InvalidWorkoutState(Exception):
    pass

@transaction.atomic
def transition_workout(workout, action):
    workout = Workout.objects.select_for_update().get(pk=workout.pk)
    now = timezone.now()
    if action == 'pause' and workout.status == 'active':
        workout.status, workout.paused_at = 'paused', now
    elif action == 'resume' and workout.status == 'paused':
        workout.accumulated_paused_seconds += max(0, int((now - workout.paused_at).total_seconds()))
        workout.paused_at, workout.status = None, 'active'
    elif action == 'finish' and workout.status in ('active', 'paused'):
        if workout.status == 'paused' and workout.paused_at:
            workout.accumulated_paused_seconds += max(0, int((now - workout.paused_at).total_seconds()))
        workout.paused_at, workout.ended_at, workout.status = None, now, 'completed'
    elif action == 'cancel' and workout.status in ('active', 'paused'):
        workout.paused_at, workout.ended_at, workout.status = None, now, 'cancelled'
    else:
        raise InvalidWorkoutState(f'Cannot {action} a {workout.get_status_display().lower()} workout.')
    workout.save()
    return workout
