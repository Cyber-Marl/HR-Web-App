from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def services(request):
    return render(request, 'services.html')

def service_detail(request, slug):
    return render(request, f'services/{slug}.html')

def contact(request):
    return render(request, 'contact.html')

from .models import NewsletterSubscriber
from django.contrib import messages
from django.shortcuts import redirect

def newsletter_signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            if not NewsletterSubscriber.objects.filter(email=email).exists():
                NewsletterSubscriber.objects.create(email=email)
                messages.success(request, 'Successfully subscribed to our newsletter!')
            else:
                messages.info(request, 'You are already subscribed.')
        else:
            messages.error(request, 'Please provide a valid email address.')
    return redirect(request.META.get('HTTP_REFERER', 'home'))

from .models import Feedback

def feedback(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        rating = request.POST.get('rating')
        message = request.POST.get('message')
        
        Feedback.objects.create(name=name, email=email, rating=rating, message=message)
        messages.success(request, "Thank you for your feedback!")
        return redirect('home')
        
    return render(request, 'feedback.html')
