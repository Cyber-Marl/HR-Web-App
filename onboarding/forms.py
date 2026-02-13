from django import forms
from django.contrib.auth.models import User
from .models import OnboardingProgram, OnboardingTask, OnboardingAssignment


class OnboardingProgramForm(forms.ModelForm):
    class Meta:
        model = OnboardingProgram
        fields = ['title', 'description', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }


class OnboardingTaskForm(forms.ModelForm):
    class Meta:
        model = OnboardingTask
        fields = ['title', 'description', 'task_type', 'order', 'is_required']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class AssignOnboardingForm(forms.ModelForm):
    employee = forms.ModelChoiceField(
        queryset=User.objects.filter(is_active=True),
        label="Assign to Employee",
        help_text="Select a user to assign this onboarding program to"
    )

    class Meta:
        model = OnboardingAssignment
        fields = ['employee', 'due_date']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }
