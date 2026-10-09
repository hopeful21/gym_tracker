from django.contrib import admin
from .models import Exercise, ExerciseFavorite, MuscleGroup, Workout, WorkoutExercise, WorkoutSet, UserPreference

@admin.register(MuscleGroup)
class MuscleGroupAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('name', 'primary_muscle_group', 'equipment', 'difficulty', 'is_featured')
    list_filter = ('primary_muscle_group', 'equipment', 'difficulty', 'is_featured')
    search_fields = ('name', 'description')

class SetInline(admin.TabularInline):
    model = WorkoutSet
    extra = 0

class WorkoutExerciseInline(admin.TabularInline):
    model = WorkoutExercise
    extra = 0

@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'started_at', 'ended_at', 'status')
    list_filter = ('status',)
    inlines = [WorkoutExerciseInline]

@admin.register(UserPreference)
class UserPreferenceAdmin(admin.ModelAdmin):
    list_display = ('user', 'weight_unit', 'preferred_rest_seconds', 'theme')

admin.site.register(WorkoutSet)
admin.site.register(ExerciseFavorite)
