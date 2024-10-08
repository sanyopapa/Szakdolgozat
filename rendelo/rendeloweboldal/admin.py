from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import RendeloUser, Doctor, Treatment, Appointment, Patient

class RendeloUserAdmin(UserAdmin):
    model = RendeloUser
    list_display = ('email', 'username', 'mobile_number', 'is_staff', 'is_active', 'is_superuser')
    list_filter = ('email', 'username', 'is_staff', 'is_active', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username', 'mobile_number')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'mobile_number', 'password1', 'password2', 'is_staff', 'is_active', 'is_superuser')}
        ),
    )
    search_fields = ('email', 'username',)
    ordering = ('email',)

admin.site.register(RendeloUser, RendeloUserAdmin)
admin.site.register(Doctor)
admin.site.register(Treatment)
admin.site.register(Appointment)
admin.site.register(Patient)