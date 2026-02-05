from django.contrib import admin
from .models import Job, Application

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'job_type', 'is_active', 'posted_at')
    list_filter = ('is_active', 'job_type', 'location')
    search_fields = ('title', 'description', 'location')
    readonly_fields = ('posted_at',)

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'job', 'status', 'applied_at')
    list_filter = ('status', 'job', 'applied_at')
    search_fields = ('full_name', 'email', 'job__title')
    readonly_fields = ('applied_at',)
    actions = ['mark_reviewed', 'mark_interview']

    def mark_reviewed(self, request, queryset):
        queryset.update(status='REVIEWED')
    mark_reviewed.short_description = "Mark selected applications as Reviewed"

    def mark_interview(self, request, queryset):
        queryset.update(status='INTERVIEW')
    mark_interview.short_description = "Mark selected applications for Interview"
