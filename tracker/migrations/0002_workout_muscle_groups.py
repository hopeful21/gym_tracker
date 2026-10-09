from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [('tracker', '0001_initial')]
    operations = [
        migrations.AddField(
            model_name='workout',
            name='muscle_groups',
            field=models.ManyToManyField(blank=True, related_name='workouts', to='tracker.musclegroup'),
        ),
    ]
