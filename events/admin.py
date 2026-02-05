from django.contrib import admin
from .models import Event, Registration

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_time', 'location', 'is_active')
    list_filter = ('is_active', 'start_time')
    search_fields = ('title', 'description')

@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('name', 'event', 'email', 'registered_at')
    list_filter = ('event',)
    search_fields = ('name', 'email')
