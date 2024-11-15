from django.urls import path
from . import views

urlpatterns = [
    path('', views.kezdooldal, name='home'),
    path('book/', views.idopontfoglalas, name='book'),  
    path('admin/', views.admin_view, name='admin'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('cancel_appointment/<str:appointment_id>/', views.cancel_appointment, name='cancel_appointment'),
    path('get_available_slots/', views.get_available_slots, name='get_available_slots'),
]