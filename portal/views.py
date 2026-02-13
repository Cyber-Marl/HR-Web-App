from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib import messages
from .models import ClientDocument
from careers.models import Job, Application
from insights.models import Article, Resource
from .forms import JobForm, ArticleForm, ResourceForm, RegistrationForm

class PortalLoginView(LoginView):
    template_name = 'portal/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        if self.request.user.is_staff:
            return '/portal/hr-dashboard/'
        return '/portal/dashboard/'

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Auto-login after registration
            messages.success(request, 'Welcome! Your account has been created successfully.')
            return redirect('portal:dashboard')
    else:
        form = RegistrationForm()
    return render(request, 'portal/register.html', {'form': form})

@login_required
def dashboard(request):
    documents = ClientDocument.objects.filter(client=request.user)
    return render(request, 'portal/dashboard.html', {'documents': documents})

def is_hr_manager(user):
    return user.is_staff

@login_required
@user_passes_test(is_hr_manager)
def hr_dashboard(request):
    jobs = Job.objects.all().order_by('-posted_at')
    articles = Article.objects.all().order_by('-created_at')
    resources = Resource.objects.all().order_by('-created_at')
    
    # Pre-format job data to avoid template rendering issues
    jobs_data = []
    for job in jobs:
        jobs_data.append({
            'id': job.id,
            'title': job.title,
            'location': job.location,
            'posted_at': job.posted_at.strftime('%b %d, %Y'),
            'deadline': job.deadline.strftime('%b %d, %Y') if job.deadline else 'None',
            'has_deadline': job.deadline is not None,
        })
    
    context = {
        'jobs': jobs,
        'jobs_data': jobs_data,
        'articles': articles,
        'resources': resources,
    }
    return render(request, 'portal/hr_dashboard.html', context)

@login_required
@user_passes_test(is_hr_manager)
def hr_add_job(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save()
            # Notify newsletter subscribers about the new job
            from core.notifications import send_new_job_notification
            send_new_job_notification(job)
            return redirect('portal:hr_dashboard')
    else:
        form = JobForm()
    return render(request, 'portal/hr_form.html', {'form': form, 'title': 'Add New Job'})

@login_required
@user_passes_test(is_hr_manager)
def hr_edit_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect('portal:hr_dashboard')
    else:
        form = JobForm(instance=job)
    return render(request, 'portal/hr_form.html', {'form': form, 'title': f'Edit Job: {job.title}'})

@login_required
@user_passes_test(is_hr_manager)
def hr_delete_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    if request.method == 'POST':
        job.delete()
        return redirect('portal:hr_dashboard')
    return render(request, 'portal/hr_delete_confirm.html', {'item': job, 'type': 'Job'})

@login_required
@user_passes_test(is_hr_manager)
def hr_job_applications(request, job_id):
    from django.db.models import Count
    from django.core.paginator import Paginator
    
    job = get_object_or_404(Job, id=job_id)
    applications = job.applications.select_related('reviewed_by').all().order_by('-applied_at')
    
    # Calculate statistics for this specific job
    stats = {
        'total': applications.count(),
        'pending': applications.filter(status='PENDING').count(),
        'reviewed': applications.filter(status='REVIEWED').count(),
        'interview': applications.filter(status='INTERVIEW').count(),
        'rejected': applications.filter(status='REJECTED').count(),
        'hired': applications.filter(status='HIRED').count(),
    }
    
    # Pagination
    paginator = Paginator(applications, 25)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    # Pre-format application data to avoid template rendering issues
    apps_data = []
    for app in page_obj:
        apps_data.append({
            'id': app.id,
            'full_name': app.full_name,
            'email': app.email,
            'phone': app.phone,
            'job_title': app.job.title if app.job else 'No Job',
            'applied_at': app.applied_at.strftime('%b %d, %Y'),
            'rating': app.rating,
            'status': app.status,
            'resume_url': app.resume.url if app.resume else '#',
            'notes': app.notes,
        })
    
    # Get all jobs for filter dropdown
    all_jobs = Job.objects.filter(is_active=True)
    
    context = {
        'applications': apps_data,
        'page_obj': page_obj,
        'stats': stats,
        'apps_by_job': [],  # Empty for single job view
        'all_jobs': all_jobs,
        'search_query': '',
        'job_filter': str(job_id),
        'selected_job_id': job.id,
        'status_filter': '',
        'date_filter': '',
        'sort_by': '-applied_at',
        'title': f'Applications for {job.title}',
        'status_choices': Application.STATUS_CHOICES,
    }
    
    return render(request, 'portal/hr_job_applications.html', context)


@login_required
@user_passes_test(is_hr_manager)
def hr_all_applications(request):
    from django.db.models import Q, Count
    from django.core.paginator import Paginator
    from datetime import datetime, timedelta
    
    applications = Application.objects.select_related('job', 'reviewed_by').all()
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        applications = applications.filter(
            Q(full_name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(job__title__icontains=search_query)
        )
    
    # Filter by job
    job_filter = request.GET.get('job', '')
    selected_job_id = None
    if job_filter:
        applications = applications.filter(job_id=job_filter)
        try:
            selected_job_id = int(job_filter)
        except ValueError:
            selected_job_id = None
    
    # Filter by status
    status_filter = request.GET.get('status', '')
    if status_filter:
        applications = applications.filter(status=status_filter)
    
    # Filter by date range
    date_filter = request.GET.get('date_range', '')
    if date_filter:
        today = datetime.now()
        if date_filter == '7':
            applications = applications.filter(applied_at__gte=today - timedelta(days=7))
        elif date_filter == '30':
            applications = applications.filter(applied_at__gte=today - timedelta(days=30))
        elif date_filter == '90':
            applications = applications.filter(applied_at__gte=today - timedelta(days=90))
    
    # Sorting
    sort_by = request.GET.get('sort', '-applied_at')
    applications = applications.order_by(sort_by)
    
    # Calculate statistics
    total_count = Application.objects.count()
    stats = {
        'total': total_count,
        'pending': Application.objects.filter(status='PENDING').count(),
        'reviewed': Application.objects.filter(status='REVIEWED').count(),
        'interview': Application.objects.filter(status='INTERVIEW').count(),
        'rejected': Application.objects.filter(status='REJECTED').count(),
        'hired': Application.objects.filter(status='HIRED').count(),
    }
    
    # Applications by job (for charts)
    apps_by_job = Job.objects.annotate(app_count=Count('applications')).order_by('-app_count')[:5]
    
    # Pagination
    paginator = Paginator(applications, 25)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    # Pre-format application data
    apps_data = []
    for app in page_obj:
        apps_data.append({
            'id': app.id,
            'full_name': app.full_name,
            'email': app.email,
            'phone': app.phone,
            'job_title': app.job.title if app.job else 'No Job',
            'applied_at': app.applied_at.strftime('%b %d, %Y'),
            'rating': app.rating,
            'status': app.status,
            'resume_url': app.resume.url if app.resume else '#',
            'notes': app.notes,
        })
    
    # Get all jobs for filter dropdown
    all_jobs = Job.objects.filter(is_active=True)
    
    context = {
        'applications': apps_data,
        'page_obj': page_obj,
        'stats': stats,
        'apps_by_job': apps_by_job,
        'all_jobs': all_jobs,
        'search_query': search_query,
        'job_filter': job_filter,
        'selected_job_id': selected_job_id,
        'status_filter': status_filter,
        'date_filter': date_filter,
        'sort_by': sort_by,
        'title': 'All Applications',
        'status_choices': Application.STATUS_CHOICES,
    }
    
    return render(request, 'portal/hr_applications.html', context)


@login_required
@user_passes_test(is_hr_manager)
def hr_update_application_rating(request, app_id):
    """AJAX endpoint to update application rating"""
    import json
    from django.http import JsonResponse
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            rating = int(data.get('rating', 0))
            app = get_object_or_404(Application, id=app_id)
            app.rating = rating
            app.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False})


@login_required
@user_passes_test(is_hr_manager)
def hr_update_application_status(request, app_id):
    """AJAX endpoint to update application status"""
    import json
    from django.http import JsonResponse
    from django.utils import timezone
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            status = data.get('status')
            app = get_object_or_404(Application, id=app_id)
            old_status = app.status
            app.status = status
            app.reviewed_by = request.user
            app.reviewed_at = timezone.now()
            app.save()
            # Send email notification about status change
            from core.notifications import send_status_change_notification
            send_status_change_notification(app, old_status)
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False})


@login_required
@user_passes_test(is_hr_manager)
def hr_add_application_note(request, app_id):
    """AJAX endpoint to add/update application notes"""
    import json
    from django.http import JsonResponse
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            notes = data.get('notes', '')
            app = get_object_or_404(Application, id=app_id)
            app.notes = notes
            app.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False})


@login_required
@user_passes_test(is_hr_manager)
def hr_export_applications(request):
    """Export applications to CSV"""
    import csv
    from django.http import HttpResponse
    from django.db.models import Q
    
    # Get filtered applications (reuse same logic as hr_all_applications)
    applications = Application.objects.select_related('job').all()
    
    # Apply same filters
    search_query = request.GET.get('search', '')
    if search_query:
        applications = applications.filter(
            Q(full_name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(job__title__icontains=search_query)
        )
    
    job_filter = request.GET.get('job', '')
    if job_filter:
        applications = applications.filter(job_id=job_filter)
    
    status_filter = request.GET.get('status', '')
    if status_filter:
        applications = applications.filter(status=status_filter)
    
    # Create CSV response
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="applications.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Name', 'Email', 'Phone', 'Job Title', 'Applied Date', 'Status', 'Rating', 'Notes'])
    
    for app in applications:
        writer.writerow([
            app.full_name,
            app.email,
            app.phone,
            app.job.title,
            app.applied_at.strftime('%Y-%m-%d'),
            app.get_status_display(),
            app.rating,
            app.notes
        ])
    
    return response



@login_required
@user_passes_test(is_hr_manager)
def hr_add_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('portal:hr_dashboard')
    else:
        form = ArticleForm()
    return render(request, 'portal/hr_form.html', {'form': form, 'title': 'Add New Article'})

@login_required
@user_passes_test(is_hr_manager)
def hr_edit_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            return redirect('portal:hr_dashboard')
    else:
        form = ArticleForm(instance=article)
    return render(request, 'portal/hr_form.html', {'form': form, 'title': f'Edit Article: {article.title}'})

@login_required
@user_passes_test(is_hr_manager)
def hr_delete_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    if request.method == 'POST':
        article.delete()
        return redirect('portal:hr_dashboard')
    return render(request, 'portal/hr_delete_confirm.html', {'item': article, 'type': 'Article'})

@login_required
@user_passes_test(is_hr_manager)
def hr_add_resource(request):
    if request.method == 'POST':
        form = ResourceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('portal:hr_dashboard')
    else:
        form = ResourceForm()
    return render(request, 'portal/hr_form.html', {'form': form, 'title': 'Add New Resource'})

@login_required
@user_passes_test(is_hr_manager)
def hr_edit_resource(request, resource_id):
    resource = get_object_or_404(Resource, id=resource_id)
    if request.method == 'POST':
        form = ResourceForm(request.POST, request.FILES, instance=resource)
        if form.is_valid():
            form.save()
            return redirect('portal:hr_dashboard')
    else:
        form = ResourceForm(instance=resource)
    return render(request, 'portal/hr_form.html', {'form': form, 'title': f'Edit Resource: {resource.title}'})

@login_required
@user_passes_test(is_hr_manager)
def hr_delete_resource(request, resource_id):
    resource = get_object_or_404(Resource, id=resource_id)
    if request.method == 'POST':
        resource.delete()
        return redirect('portal:hr_dashboard')
    return render(request, 'portal/hr_delete_confirm.html', {'item': resource, 'type': 'Resource'})


@login_required
@user_passes_test(is_hr_manager)
def hr_analytics(request):
    """HR Analytics Dashboard with charts and metrics"""
    from django.db.models import Count, Avg, F
    from django.db.models.functions import TruncMonth
    from datetime import datetime, timedelta
    from django.utils import timezone
    from core.models import NewsletterSubscriber
    from events.models import Event, Registration
    from onboarding.models import OnboardingAssignment

    # Hiring funnel counts
    funnel = {
        'pending': Application.objects.filter(status='PENDING').count(),
        'reviewed': Application.objects.filter(status='REVIEWED').count(),
        'interview': Application.objects.filter(status='INTERVIEW').count(),
        'hired': Application.objects.filter(status='HIRED').count(),
        'rejected': Application.objects.filter(status='REJECTED').count(),
    }

    # Applications over last 6 months
    six_months_ago = timezone.now() - timedelta(days=180)
    timeline_qs = (
        Application.objects
        .filter(applied_at__gte=six_months_ago)
        .annotate(month=TruncMonth('applied_at'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )
    timeline = []
    for item in timeline_qs:
        timeline.append({
            'month': item['month'].strftime('%b %Y'),
            'count': item['count'],
        })
    # If no data, provide at least the current month
    if not timeline:
        timeline = [{'month': timezone.now().strftime('%b %Y'), 'count': 0}]

    # Top jobs by application count
    top_jobs = (
        Job.objects
        .annotate(app_count=Count('applications'))
        .order_by('-app_count')[:5]
    )
    top_jobs_data = [{'title': j.title, 'app_count': j.app_count} for j in top_jobs]

    # Event registration stats
    event_stats = (
        Event.objects
        .filter(is_active=True)
        .annotate(reg_count=Count('registrations'))
        .order_by('-reg_count')[:5]
    )
    event_stats_data = [{'title': e.title, 'reg_count': e.reg_count} for e in event_stats]

    # Average time to hire (days from application to hired status)
    hired_apps = Application.objects.filter(status='HIRED', reviewed_at__isnull=False)
    if hired_apps.exists():
        total_days = 0
        count = 0
        for app in hired_apps:
            delta = (app.reviewed_at - app.applied_at).days
            total_days += delta
            count += 1
        avg_time_to_hire = round(total_days / count) if count > 0 else 0
    else:
        avg_time_to_hire = 0

    context = {
        'total_applications': Application.objects.count(),
        'open_positions': Job.objects.filter(is_active=True).count(),
        'avg_time_to_hire': avg_time_to_hire,
        'subscriber_count': NewsletterSubscriber.objects.filter(is_active=True).count(),
        'total_events': Event.objects.filter(is_active=True).count(),
        'onboarding_active': OnboardingAssignment.objects.filter(is_completed=False).count(),
        'funnel': funnel,
        'timeline': timeline,
        'top_jobs': top_jobs_data,
        'event_stats': event_stats_data,
    }
    return render(request, 'portal/hr_analytics.html', context)
