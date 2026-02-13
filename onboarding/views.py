from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from .models import OnboardingProgram, OnboardingTask, OnboardingAssignment, TaskCompletion
from .forms import OnboardingProgramForm, OnboardingTaskForm, AssignOnboardingForm


def is_hr_manager(user):
    return user.is_staff


# ─── HR Management Views ───────────────────────────────────────────────────────

@login_required
@user_passes_test(is_hr_manager)
def program_list(request):
    programs = OnboardingProgram.objects.all()
    # Pre-compute stats for each program
    programs_data = []
    for program in programs:
        programs_data.append({
            'id': program.id,
            'title': program.title,
            'description': program.description,
            'is_active': program.is_active,
            'task_count': program.tasks.count(),
            'assignment_count': program.assignments.count(),
            'created_at': program.created_at.strftime('%b %d, %Y'),
        })
    return render(request, 'onboarding/program_list.html', {'programs': programs_data})


@login_required
@user_passes_test(is_hr_manager)
def program_create(request):
    if request.method == 'POST':
        form = OnboardingProgramForm(request.POST)
        if form.is_valid():
            program = form.save(commit=False)
            program.created_by = request.user
            program.save()
            messages.success(request, f'Program "{program.title}" created successfully!')
            return redirect('onboarding:program_detail', program_id=program.id)
    else:
        form = OnboardingProgramForm()
    return render(request, 'onboarding/program_form.html', {'form': form, 'title': 'Create Onboarding Program'})


@login_required
@user_passes_test(is_hr_manager)
def program_edit(request, program_id):
    program = get_object_or_404(OnboardingProgram, id=program_id)
    if request.method == 'POST':
        form = OnboardingProgramForm(request.POST, instance=program)
        if form.is_valid():
            form.save()
            messages.success(request, f'Program "{program.title}" updated!')
            return redirect('onboarding:program_detail', program_id=program.id)
    else:
        form = OnboardingProgramForm(instance=program)
    return render(request, 'onboarding/program_form.html', {'form': form, 'title': f'Edit: {program.title}'})


@login_required
@user_passes_test(is_hr_manager)
def program_detail(request, program_id):
    program = get_object_or_404(OnboardingProgram, id=program_id)
    tasks = program.tasks.all()
    assignments = program.assignments.select_related('employee').all()

    # Pre-compute assignment data
    assignments_data = []
    for assignment in assignments:
        assignments_data.append({
            'id': assignment.id,
            'employee_name': assignment.employee.get_full_name() or assignment.employee.username,
            'assigned_at': assignment.assigned_at.strftime('%b %d, %Y'),
            'due_date': assignment.due_date.strftime('%b %d, %Y') if assignment.due_date else 'No deadline',
            'progress': assignment.progress_percent(),
            'completed_count': assignment.completed_count(),
            'total_tasks': tasks.count(),
            'is_completed': assignment.is_completed,
        })

    # Pre-compute task data
    tasks_data = []
    for task in tasks:
        tasks_data.append({
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'task_type': task.get_task_type_display(),
            'is_required': task.is_required,
            'order': task.order,
        })

    context = {
        'program': program,
        'tasks': tasks_data,
        'assignments': assignments_data,
    }
    return render(request, 'onboarding/program_detail.html', context)


@login_required
@user_passes_test(is_hr_manager)
def add_task(request, program_id):
    program = get_object_or_404(OnboardingProgram, id=program_id)
    if request.method == 'POST':
        form = OnboardingTaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.program = program
            task.save()
            messages.success(request, f'Task "{task.title}" added!')
            return redirect('onboarding:program_detail', program_id=program.id)
    else:
        # Default order to next available
        next_order = program.tasks.count() + 1
        form = OnboardingTaskForm(initial={'order': next_order})
    return render(request, 'onboarding/program_form.html', {
        'form': form,
        'title': f'Add Task to: {program.title}',
        'program': program,
    })


@login_required
@user_passes_test(is_hr_manager)
def assign_program(request, program_id):
    program = get_object_or_404(OnboardingProgram, id=program_id)
    if request.method == 'POST':
        form = AssignOnboardingForm(request.POST)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.program = program
            assignment.assigned_by = request.user

            # Check if already assigned
            if OnboardingAssignment.objects.filter(program=program, employee=assignment.employee).exists():
                messages.warning(request, f'This program is already assigned to {assignment.employee.username}.')
                return redirect('onboarding:program_detail', program_id=program.id)

            assignment.save()

            # Create TaskCompletion entries for each task
            for task in program.tasks.all():
                TaskCompletion.objects.create(assignment=assignment, task=task)

            messages.success(request, f'Program assigned to {assignment.employee.username}!')
            return redirect('onboarding:program_detail', program_id=program.id)
    else:
        form = AssignOnboardingForm()
    return render(request, 'onboarding/program_form.html', {
        'form': form,
        'title': f'Assign: {program.title}',
        'program': program,
    })


@login_required
@user_passes_test(is_hr_manager)
def assignment_progress(request, assignment_id):
    assignment = get_object_or_404(OnboardingAssignment, id=assignment_id)
    completions = assignment.task_completions.select_related('task').all()

    completions_data = []
    for c in completions:
        completions_data.append({
            'id': c.id,
            'task_title': c.task.title,
            'task_description': c.task.description,
            'task_type': c.task.get_task_type_display(),
            'is_required': c.task.is_required,
            'is_completed': c.is_completed,
            'completed_at': c.completed_at.strftime('%b %d, %Y %H:%M') if c.completed_at else None,
            'notes': c.notes,
        })

    context = {
        'assignment': assignment,
        'completions': completions_data,
        'progress': assignment.progress_percent(),
        'employee_name': assignment.employee.get_full_name() or assignment.employee.username,
        'program_title': assignment.program.title,
    }
    return render(request, 'onboarding/assignment_progress.html', context)


# ─── Employee-Facing Views ─────────────────────────────────────────────────────

@login_required
def my_onboarding(request):
    assignments = OnboardingAssignment.objects.filter(
        employee=request.user
    ).select_related('program')

    assignments_data = []
    for assignment in assignments:
        completions = assignment.task_completions.select_related('task').all()
        tasks_data = []
        for c in completions:
            tasks_data.append({
                'completion_id': c.id,
                'title': c.task.title,
                'description': c.task.description,
                'task_type': c.task.get_task_type_display(),
                'is_required': c.task.is_required,
                'is_completed': c.is_completed,
                'completed_at': c.completed_at.strftime('%b %d, %Y') if c.completed_at else None,
            })

        assignments_data.append({
            'id': assignment.id,
            'program_title': assignment.program.title,
            'program_description': assignment.program.description,
            'progress': assignment.progress_percent(),
            'completed_count': assignment.completed_count(),
            'total_tasks': assignment.program.tasks.count(),
            'due_date': assignment.due_date.strftime('%b %d, %Y') if assignment.due_date else None,
            'is_completed': assignment.is_completed,
            'tasks': tasks_data,
        })

    return render(request, 'onboarding/my_onboarding.html', {'assignments': assignments_data})


@login_required
def complete_task(request, completion_id):
    """AJAX endpoint to mark a task as complete"""
    import json

    completion = get_object_or_404(TaskCompletion, id=completion_id, assignment__employee=request.user)

    if request.method == 'POST':
        try:
            completion.is_completed = True
            completion.completed_at = timezone.now()
            completion.save()

            # Check if all tasks in the assignment are now complete
            assignment = completion.assignment
            total = assignment.program.tasks.count()
            completed = assignment.task_completions.filter(is_completed=True).count()

            if completed >= total:
                assignment.is_completed = True
                assignment.completed_at = timezone.now()
                assignment.save()

            return JsonResponse({
                'success': True,
                'progress': assignment.progress_percent(),
                'completed_count': completed,
                'total_tasks': total,
                'all_complete': assignment.is_completed,
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'POST required'})
