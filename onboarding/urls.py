from django.urls import path
from . import views

app_name = 'onboarding'

urlpatterns = [
    # HR Management
    path('programs/', views.program_list, name='program_list'),
    path('programs/create/', views.program_create, name='program_create'),
    path('programs/<int:program_id>/', views.program_detail, name='program_detail'),
    path('programs/<int:program_id>/edit/', views.program_edit, name='program_edit'),
    path('programs/<int:program_id>/add-task/', views.add_task, name='add_task'),
    path('programs/<int:program_id>/assign/', views.assign_program, name='assign_program'),
    path('assignments/<int:assignment_id>/progress/', views.assignment_progress, name='assignment_progress'),

    # Employee-facing
    path('my-onboarding/', views.my_onboarding, name='my_onboarding'),
    path('complete-task/<int:completion_id>/', views.complete_task, name='complete_task'),
]
