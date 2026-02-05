from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from .models import ClientDocument

class PortalLoginView(LoginView):
    template_name = 'portal/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return '/portal/dashboard/'

@login_required
def dashboard(request):
    documents = ClientDocument.objects.filter(client=request.user)
    return render(request, 'portal/dashboard.html', {'documents': documents})
