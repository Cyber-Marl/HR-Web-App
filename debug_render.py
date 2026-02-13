import os
import django
from django.template.loader import render_to_string
from django.conf import settings

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'strategic_synergy.settings')
django.setup()

from careers.models import Application, Job
from portal.views import Application as ViewApplication # Using Application model

def debug_render():
    app = Application.objects.first()
    if not app:
        # Create a dummy one if none exists
        job = Job.objects.first()
        if not job:
            job = Job.objects.create(title="Test Job", location="Virtual")
        app = Application(id=1, full_name="Test User", job=job, status='PENDING')
    
    status_choices = Application.STATUS_CHOICES
    print(f"DEBUG: status_choices = {status_choices}")
    
    apps_data = [{
        'id': app.id,
        'full_name': app.full_name,
        'email': app.email,
        'phone': app.phone,
        'job_title': app.job.title if app.job else 'No Job',
        'applied_at': app.applied_at.strftime('%b %d, %Y') if hasattr(app.applied_at, 'strftime') else 'Feb 05, 2026',
        'rating': app.rating,
        'status': app.status,
        'resume_url': app.resume.url if hasattr(app, 'resume') and app.resume else '#',
        'notes': app.notes if hasattr(app, 'notes') else '',
    }]
    
    ctx = {
        'applications': apps_data,
        'status_choices': status_choices,
        'stats': {'total':1, 'pending':1, 'reviewed':0, 'interview':0, 'hired':0},
        'title': 'Test',
        'page_obj': type('obj', (object,), {'paginator': type('p', (object,), {'count':1})(), 'has_other_pages': False})(),
    }
    
    html = render_to_string('portal/hr_applications.html', ctx)
    with open('render_debug.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("DEBUG: Rendered to render_debug.html")

if __name__ == "__main__":
    debug_render()
