from django.urls import path
from . import views

app_name = 'insights'

urlpatterns = [
    path('', views.article_list, name='article_list'),
    path('resources/', views.resource_list, name='resource_list'),
    path('<slug:slug>/', views.article_detail, name='article_detail'),
]
