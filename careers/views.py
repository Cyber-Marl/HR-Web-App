from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Job, Application

from django.db.models import Q

def job_list(request):
    query = request.GET.get('q')
    job_type = request.GET.get('job_type')
    location = request.GET.get('location')
    
    jobs = Job.objects.filter(is_active=True)
    
    if query:
        jobs = jobs.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query) | 
            Q(requirements__icontains=query)
        )
    
    if job_type:
        jobs = jobs.filter(job_type=job_type)
        
    if location:
        jobs = jobs.filter(location=location)

    locations = Job.objects.filter(is_active=True).values_list('location', flat=True).distinct()
    job_types = Job.JOB_TYPES

    context = {
        'jobs': jobs,
        'locations': locations,
        'job_types': job_types,
        'query': query,
        'selected_job_type': job_type,
        'selected_location': location,
    }
    return render(request, 'careers/job_list.html', context)

def job_detail(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    return render(request, 'careers/job_detail.html', {'job': job})

def apply_job(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        linkedin_url = request.POST.get('linkedin_url')
        cover_letter = request.POST.get('cover_letter')
        resume = request.FILES.get('resume')

        if resume:
            application = Application.objects.create(
                job=job,
                full_name=full_name,
                email=email,
                phone=phone,
                linkedin_url=linkedin_url,
                cover_letter=cover_letter,
                resume=resume
            )
            # Send confirmation email to applicant
            from core.notifications import send_application_confirmation
            send_application_confirmation(application)
            messages.success(request, f"Application for {job.title} submitted successfully!")
            return redirect('careers:job_list') # Ideally redirect to a success page or back to list
        else:
            messages.error(request, "Please upload your resume.")

    return render(request, 'careers/job_detail.html', {'job': job}) 
