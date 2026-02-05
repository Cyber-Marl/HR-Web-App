from django.db import models

class Article(models.Model):
    CATEGORY_CHOICES = [
        ('LEADERSHIP', 'Leadership'),
        ('TALENT', 'Talent Acquisition'),
        ('CULTURE', 'Company Culture'),
        ('STRATEGY', 'Strategy'),
        ('TECH', 'HR Tech'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, help_text="Unique URL identifier for the article")
    author = models.CharField(max_length=100, default="Strategic Synergy Team")
    # For a real rich text experience, we'd use django-ckeditor or similar, but TextField works for now with line breaks
    content = models.TextField()
    image = models.ImageField(upload_to='insights/images/', blank=True, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='LEADERSHIP')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']

class Resource(models.Model):
    RESOURCE_TYPES = [
        ('TEMPLATE', 'Template'),
        ('CHECKLIST', 'Checklist'),
        ('GUIDE', 'Guide'),
        ('POLICY', 'Policy Document'),
    ]

    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='resources/')
    description = models.TextField(blank=True)
    resource_type = models.CharField(max_length=20, choices=RESOURCE_TYPES, default='GUIDE')
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
