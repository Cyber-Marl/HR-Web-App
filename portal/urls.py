from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'portal'

urlpatterns = [
    path('login/', views.PortalLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
