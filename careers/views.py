from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Job, Application

def job_list(request):
    jobs = Job.objects.filter(is_active=True)
    return render(request, 'careers/job_list.html', {'jobs': jobs})

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
            Application.objects.create(
                job=job,
                full_name=full_name,
                email=email,
                phone=phone,
                linkedin_url=linkedin_url,
                cover_letter=cover_letter,
                resume=resume
            )
            messages.success(request, f"Application for {job.title} submitted successfully!")
            return redirect('careers:job_list') # Ideally redirect to a success page or back to list
        else:
            messages.error(request, "Please upload your resume.")

    return render(request, 'careers/job_detail.html', {'job': job}) 
