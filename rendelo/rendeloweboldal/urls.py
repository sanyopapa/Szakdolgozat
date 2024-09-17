from django.urls import path
from . import views

urlpatterns = [
    path('', views.kezdooldal, name='home'),  
    path('book/', views.idopontfoglalas, name='book'),
    path('admin-view/', views.admin_view, name='admin_view'),  
]