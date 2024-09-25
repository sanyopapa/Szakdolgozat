from django.urls import path
from . import views
from .views import register_view, login_view

urlpatterns = [
    path('', views.kezdooldal, name='home'),  
    path('book/', views.idopontfoglalas, name='book'),
    path('admin-view/', views.admin_view, name='admin_view'), 
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'), 
]