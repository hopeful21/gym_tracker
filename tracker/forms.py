from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import MuscleGroup
from .models import Exercise, UserPreference, Workout, WorkoutSet

class WorkoutStartForm(forms.ModelForm):
    class Meta:
        model = Workout
        fields = ['title', 'muscle_groups']
        widgets = {'title': forms.TextInput(attrs={'placeholder': 'e.g. Upper body strength'}), 'muscle_groups': forms.CheckboxSelectMultiple}
        labels = {'muscle_groups': 'Muscle groups'}
    def clean_muscle_groups(self):
        groups = self.cleaned_data['muscle_groups']
        if not groups:
            raise forms.ValidationError('Choose at least one muscle group for this workout.')
        return groups

class ExerciseFilterForm(forms.Form):
    q = forms.CharField(required=False, label='Search exercises')
    muscle = forms.CharField(required=False)
    equipment = forms.CharField(required=False)
    difficulty = forms.ChoiceField(required=False, choices=[('', 'Any level')] + Exercise.DIFFICULTIES)

class SetForm(forms.ModelForm):
    class Meta:
        model = WorkoutSet
        fields = ['set_number', 'repetitions', 'weight']
        widgets = {f: forms.NumberInput(attrs={'min': '0', 'step': 'any'}) for f in ['set_number', 'repetitions', 'weight']}

class PreferenceForm(forms.ModelForm):
    class Meta:
        model = UserPreference
        fields = ['weight_unit', 'preferred_rest_seconds', 'theme', 'confirm_delete']


class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username',)
