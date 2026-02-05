from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Event, Registration

def event_list(request):
    events = Event.objects.filter(is_active=True).order_by('start_time')
    return render(request, 'events/event_list.html', {'events': events})

def event_detail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        
        Registration.objects.create(event=event, name=name, email=email, phone=phone)
        messages.success(request, f"You have successfully registered for {event.title}!")
        return redirect('events:event_list')

    return render(request, 'events/event_detail.html', {'event': event})
