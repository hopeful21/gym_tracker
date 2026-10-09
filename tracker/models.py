from datetime import timedelta
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone


class MuscleGroup(models.Model):
    name = models.CharField(max_length=40, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    image = models.CharField(max_length=120, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Exercise(models.Model):
    DIFFICULTIES = [('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced')]
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    primary_muscle_group = models.ForeignKey(MuscleGroup, on_delete=models.PROTECT, related_name='primary_exercises')
    secondary_muscle_groups = models.ManyToManyField(MuscleGroup, blank=True, related_name='secondary_exercises')
    equipment = models.CharField(max_length=80, default='Dumbbells')
    difficulty = models.CharField(max_length=20, choices=DIFFICULTIES, default='beginner')
    instructions = models.TextField(blank=True)
    image = models.CharField(max_length=120, blank=True)
    demo_url = models.URLField(blank=True)
    is_featured = models.BooleanField(default=False)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Workout(models.Model):
    user = models.ForeignKey('auth.User', null=True, blank=True, on_delete=models.CASCADE, related_name='workouts')
    STATUSES = [('active', 'Workout in progress'), ('paused', 'Paused'), ('completed', 'Completed'), ('cancelled', 'Cancelled')]
    title = models.CharField(max_length=120, default='Strength session')
    started_at = models.DateTimeField(default=timezone.now, db_index=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=12, choices=STATUSES, default='active', db_index=True)
    notes = models.TextField(blank=True)
    paused_at = models.DateTimeField(null=True, blank=True)
    accumulated_paused_seconds = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    muscle_groups = models.ManyToManyField('MuscleGroup', blank=True, related_name='workouts')

    class Meta:
        ordering = ['-started_at']
        constraints = [models.CheckConstraint(condition=models.Q(accumulated_paused_seconds__gte=0), name='nonnegative_paused_seconds')]

    def __str__(self):
        return self.title

    @property
    def elapsed_seconds(self):
        stop = self.ended_at or (self.paused_at if self.status == 'paused' and self.paused_at else timezone.now())
        return max(0, int((stop - self.started_at).total_seconds()) - self.accumulated_paused_seconds)

    @property
    def duration(self):
        return timedelta(seconds=self.elapsed_seconds)

    @property
    def duration_display(self):
        seconds = self.elapsed_seconds
        return f'{seconds // 3600:02}:{(seconds % 3600) // 60:02}:{seconds % 60:02}'

    @property
    def volume(self):
        from django.db.models import F, Sum
        return WorkoutSet.objects.filter(workout_exercise__workout=self, is_completed=True).aggregate(v=Sum(F('weight') * F('repetitions')))['v'] or 0


class WorkoutExercise(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE, related_name='workout_exercises')
    exercise = models.ForeignKey(Exercise, on_delete=models.PROTECT, related_name='workout_entries')
    order = models.PositiveSmallIntegerField(default=0)
    class Meta:
        ordering = ['order', 'id']
        constraints = [models.UniqueConstraint(fields=['workout', 'exercise'], name='unique_exercise_per_workout')]

    def __str__(self):
        return f'{self.exercise} · {self.workout}'


class WorkoutSet(models.Model):
    workout_exercise = models.ForeignKey(WorkoutExercise, on_delete=models.CASCADE, related_name='sets')
    set_number = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(99)])
    repetitions = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(999)])
    weight = models.DecimalField(max_digits=7, decimal_places=2, validators=[MinValueValidator(0)])
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    class Meta:
        ordering = ['set_number']
        constraints = [models.UniqueConstraint(fields=['workout_exercise', 'set_number'], name='unique_set_per_exercise')]

    @property
    def volume(self):
        return self.weight * self.repetitions


class UserPreference(models.Model):
    user = models.OneToOneField('auth.User', null=True, blank=True, on_delete=models.CASCADE, related_name='fitness_preferences')
    WEIGHT_UNITS = [('kg', 'Kilograms'), ('lb', 'Pounds')]
    THEME_CHOICES = [('dark', 'Dark'), ('light', 'Light'), ('system', 'System')]
    weight_unit = models.CharField(max_length=2, choices=WEIGHT_UNITS, default='kg')
    preferred_rest_seconds = models.PositiveSmallIntegerField(default=60, validators=[MinValueValidator(15), MaxValueValidator(600)])
    theme = models.CharField(max_length=10, choices=THEME_CHOICES, default='dark')
    confirm_delete = models.BooleanField(default=True)

    @classmethod
    def current(cls, user):
        obj, _ = cls.objects.get_or_create(user=user)
        return obj


class ExerciseFavorite(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='exercise_favorites')
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name='favorites')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['exercise__name']
        constraints = [models.UniqueConstraint(fields=['user', 'exercise'], name='unique_user_exercise_favorite')]

    def __str__(self):
        return f'{self.user} · {self.exercise}'
