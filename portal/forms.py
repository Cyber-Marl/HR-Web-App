from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from careers.models import Job
from insights.models import Article, Resource

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Required. Enter a valid email address.")
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already registered.")
        return email

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'location', 'job_type', 'description', 'requirements', 'salary_range', 'deadline', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'requirements': forms.Textarea(attrs={'rows': 4}),
            'deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'slug', 'author', 'content', 'image', 'category', 'is_published']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 10}),
        }

class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ['title', 'file', 'description', 'resource_type', 'is_public']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
