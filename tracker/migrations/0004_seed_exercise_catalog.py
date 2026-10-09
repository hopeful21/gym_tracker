from django.db import migrations


MUSCLE_GROUPS = {
    'Thighs': 'thighs',
    'Back': 'back',
    'Shoulders': 'shoulders',
    'Biceps': 'biceps',
    'Forearms': 'forearms',
    'Wrists': 'wrists',
    'Calves': 'calves',
    'Chest': 'chest',
}

EXERCISES = [
    ('Goblet squat', 'Thighs', 'Dumbbells', 'beginner', 'goblet-squat.jpeg', 'Hold one dumbbell at chest height and squat with a controlled tempo.'),
    ('Dumbbell Romanian deadlift', 'Thighs', 'Dumbbells', 'intermediate', 'dumbbell-romanian-deadlift.jpeg', 'Hinge at the hips while keeping a neutral spine.'),
    ('Dumbbell row', 'Back', 'Dumbbells', 'beginner', 'dumbbell-row.jpeg', 'Brace one hand on a bench and row the weight toward your hip.'),
    ('Renegade row', 'Back', 'Dumbbells', 'advanced', 'renegade-row.jpeg', 'Hold a strong plank and row one dumbbell at a time.'),
    ('Dumbbell shoulder press', 'Shoulders', 'Dumbbells', 'beginner', 'dumbbell-shoulder-press.jpeg', 'Press both weights overhead without arching your lower back.'),
    ('Dumbbell lateral raise', 'Shoulders', 'Dumbbells', 'beginner', 'dumbbell-lateral-raise.jpeg', 'Raise light weights to shoulder height with soft elbows.'),
    ('Biceps curl', 'Biceps', 'Dumbbells', 'beginner', 'biceps-curl.jpeg', 'Curl both weights while keeping your elbows close to your sides.'),
    ('Hammer curl', 'Biceps', 'Dumbbells', 'beginner', 'hammer-curl.jpeg', 'Curl with palms facing one another throughout the movement.'),
    ('Farmer carry', 'Forearms', 'Dumbbells', 'intermediate', 'farmer-carry.jpeg', 'Walk tall while carrying heavy weights at your sides.'),
    ('Wrist curl', 'Wrists', 'Dumbbells', 'beginner', 'wrist-curl.jpeg', 'Rest your forearm on a bench and flex the wrist through a comfortable range.'),
    ('Reverse wrist curl', 'Forearms', 'Dumbbells', 'beginner', 'reverse-wrist-curl.jpeg', 'Lift the back of your hand while your forearm stays supported.'),
    ('Standing calf raise', 'Calves', 'Dumbbells', 'beginner', 'standing-calf-raise.jpeg', 'Rise onto the balls of your feet, pause, then lower slowly.'),
    ('Dumbbell chest press', 'Chest', 'Dumbbells', 'beginner', 'dumbbell-chest-press.jpeg', 'Press from the chest with wrists stacked over elbows.'),
    ('Dumbbell fly', 'Chest', 'Dumbbells', 'intermediate', 'dumbbell-fly.jpeg', 'Lower the weights in a wide arc while maintaining a slight elbow bend.'),
    ('Wide push-up', 'Chest', 'Bodyweight', 'beginner', 'wide-push-up.jpeg', 'Set your hands wider than shoulder width, brace your core, and lower your chest under control.'),
]


def seed_catalog(apps, schema_editor):
    MuscleGroup = apps.get_model('tracker', 'MuscleGroup')
    Exercise = apps.get_model('tracker', 'Exercise')
    database = schema_editor.connection.alias

    groups = {}
    for name, slug in MUSCLE_GROUPS.items():
        group, _ = MuscleGroup.objects.using(database).get_or_create(
            name=name,
            defaults={'slug': slug},
        )
        groups[name] = group

    for name, muscle, equipment, difficulty, image, instructions in EXERCISES:
        Exercise.objects.using(database).get_or_create(
            name=name,
            defaults={
                'primary_muscle_group': groups[muscle],
                'equipment': equipment,
                'difficulty': difficulty,
                'description': f'A focused {difficulty} movement for your {muscle.lower()}.',
                'instructions': instructions,
                'image': f'exercises/{image}',
            },
        )


class Migration(migrations.Migration):
    dependencies = [('tracker', '0003_rename_is_favorite_exercise_is_featured_and_more')]

    operations = [migrations.RunPython(seed_catalog, migrations.RunPython.noop)]
