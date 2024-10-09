from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from .views import register_view, login_view

urlpatterns = [
    path('', views.kezdooldal, name='home'),
    path('book/', views.idopontfoglalas, name='book'),
    path('admin-view/', views.admin_view, name='admin_view'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)