from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.kezdooldal, name='home'),
    path('book/', views.idopontfoglalas, name='book'),  
    path('custom_admin/', views.admin_view, name='admin_view'),  
    path('custom_admin/add_treatment/', views.add_treatment, name='add_treatment'),
    path('custom_admin/edit_treatment/<uuid:treatment_id>/', views.edit_treatment, name='edit_treatment'),
    path('custom_admin/delete_treatment/<uuid:treatment_id>/', views.delete_treatment, name='delete_treatment'),
    path('custom_admin/add_doctor/', views.add_doctor, name='add_doctor'),
    path('custom_admin/edit_doctor/<str:doctor_id>/', views.edit_doctor, name='edit_doctor'),
    path('custom_admin/delete_doctor/<str:doctor_id>/', views.delete_doctor, name='delete_doctor'),
    path('custom_admin/edit_user/<str:user_id>/', views.edit_user, name='edit_user'),
    path('custom_admin/delete_user/<str:user_id>/', views.delete_user, name='delete_user'),
    path('custom_admin/add_admin_user/', views.add_admin_user, name='add_admin_user'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('cancel_appointment/<str:appointment_id>/', views.cancel_appointment, name='cancel_appointment'),
    path('get_available_slots/', views.get_available_slots, name='get_available_slots'),
    path('get_earliest_slot/', views.get_earliest_slot, name='get_earliest_slot'),
    path('patients/', views.patients_view, name='patients'),  
    path('patients/<str:patient_id>/', views.patient_detail_view, name='patient_detail'),  
    path('appointments_today/', views.appointments_today_view, name='appointments_today'),  
    path('working_hours/', views.working_hours_view, name='working_hours'),  
    path('edit_appointment/<str:appointment_id>/', views.edit_appointment, name='edit_appointment'),  
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)