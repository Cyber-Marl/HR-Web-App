from django.db import models
from django.contrib.auth.models import User


class OnboardingProgram(models.Model):
    """A named onboarding program (e.g., 'Software Engineer Onboarding')"""
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_programs')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def task_count(self):
        return self.tasks.count()

    class Meta:
        ordering = ['-created_at']


class OnboardingTask(models.Model):
    """Individual checklist item within a program"""
    TASK_TYPES = [
        ('DOCUMENT', 'Document Upload'),
        ('ACKNOWLEDGE', 'Policy Acknowledgement'),
        ('TRAINING', 'Training / Course'),
        ('FORM', 'Complete a Form'),
        ('GENERAL', 'General Task'),
    ]

    program = models.ForeignKey(OnboardingProgram, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    task_type = models.CharField(max_length=20, choices=TASK_TYPES, default='GENERAL')
    order = models.PositiveIntegerField(default=0, help_text="Display order within the program")
    is_required = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} ({self.program.title})"

    class Meta:
        ordering = ['order', 'id']


class OnboardingAssignment(models.Model):
    """Links a program to a new hire"""
    program = models.ForeignKey(OnboardingProgram, on_delete=models.CASCADE, related_name='assignments')
    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='onboarding_assignments')
    assigned_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='assigned_onboardings')
    assigned_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.employee.username} - {self.program.title}"

    def progress_percent(self):
        total = self.program.tasks.count()
        if total == 0:
            return 100
        completed = self.task_completions.filter(is_completed=True).count()
        return int((completed / total) * 100)

    def completed_count(self):
        return self.task_completions.filter(is_completed=True).count()

    class Meta:
        ordering = ['-assigned_at']
        unique_together = ['program', 'employee']


class TaskCompletion(models.Model):
    """Tracks completion of individual tasks per assignment"""
    assignment = models.ForeignKey(OnboardingAssignment, on_delete=models.CASCADE, related_name='task_completions')
    task = models.ForeignKey(OnboardingTask, on_delete=models.CASCADE, related_name='completions')
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        status = "✓" if self.is_completed else "○"
        return f"{status} {self.task.title}"

    class Meta:
        unique_together = ['assignment', 'task']
