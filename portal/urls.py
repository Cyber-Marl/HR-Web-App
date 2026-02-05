from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'portal'

urlpatterns = [
    path('login/', views.PortalLoginView.as_view(), name='login'),
    path('register/', views.register, name='register'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Password Reset
    path('password-reset/', 
         auth_views.PasswordResetView.as_view(template_name='portal/password_reset_form.html'), 
         name='password_reset'),
    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(template_name='portal/password_reset_done.html'), 
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name='portal/password_reset_confirm.html'), 
         name='password_reset_confirm'),
    path('password-reset-complete/', 
         auth_views.PasswordResetCompleteView.as_view(template_name='portal/password_reset_complete.html'), 
         name='password_reset_complete'),
    
    # HR Dashboard
    path('hr-dashboard/', views.hr_dashboard, name='hr_dashboard'),
    
    # Jobs
    path('hr-dashboard/add-job/', views.hr_add_job, name='hr_add_job'),
    path('hr-dashboard/edit-job/<int:job_id>/', views.hr_edit_job, name='hr_edit_job'),
    path('hr-dashboard/delete-job/<int:job_id>/', views.hr_delete_job, name='hr_delete_job'),
    path('hr-dashboard/job-applications/<int:job_id>/', views.hr_job_applications, name='hr_job_applications'),
    path('hr-dashboard/all-applications/', views.hr_all_applications, name='hr_all_applications'),
    
    # Application Management AJAX Endpoints
    path('hr-applications/update-rating/<int:app_id>/', views.hr_update_application_rating, name='hr_update_rating'),
    path('hr-applications/update-status/<int:app_id>/', views.hr_update_application_status, name='hr_update_status'),
    path('hr-applications/add-note/<int:app_id>/', views.hr_add_application_note, name='hr_add_note'),
    path('hr-applications/export/', views.hr_export_applications, name='hr_export_applications'),

    # Articles
    path('hr-dashboard/add-article/', views.hr_add_article, name='hr_add_article'),
    path('hr-dashboard/edit-article/<int:article_id>/', views.hr_edit_article, name='hr_edit_article'),
    path('hr-dashboard/delete-article/<int:article_id>/', views.hr_delete_article, name='hr_delete_article'),

    # Resources
    path('hr-dashboard/add-resource/', views.hr_add_resource, name='hr_add_resource'),
    path('hr-dashboard/edit-resource/<int:resource_id>/', views.hr_edit_resource, name='hr_edit_resource'),
    path('hr-dashboard/delete-resource/<int:resource_id>/', views.hr_delete_resource, name='hr_delete_resource'),
]
