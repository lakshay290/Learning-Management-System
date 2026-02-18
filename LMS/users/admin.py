from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('role', 'is_teacher')}),
    )
    list_display = ('username', 'email', 'role', 'is_teacher', 'is_staff')
    list_filter = BaseUserAdmin.list_filter + ('role', 'is_teacher')
    search_fields = BaseUserAdmin.search_fields + ('role',)
