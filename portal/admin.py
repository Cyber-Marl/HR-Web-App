from django.contrib import admin
from .models import ClientDocument

@admin.register(ClientDocument)
class ClientDocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'client', 'uploaded_at')
    list_filter = ('client', 'uploaded_at')
    search_fields = ('title', 'client__username', 'client__email')
