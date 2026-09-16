from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, MechanicProfile, AdvisorProfile


@admin.register(User)
class SmartGarageUserAdmin(UserAdmin):
    list_display = ('username', 'get_full_name', 'email', 'role', 'phone', 'is_active', 'created_at')
    list_filter = ('role', 'is_active', 'is_verified')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'phone')
    fieldsets = UserAdmin.fieldsets + (
        ('Smart Garage Info', {'fields': ('role', 'phone', 'profile_image', 'is_verified')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Smart Garage Info', {'fields': ('role', 'phone', 'email')}),
    )


@admin.register(MechanicProfile)
class MechanicProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialization', 'experience_years', 'is_available', 'rating', 'jobs_completed')
    list_filter = ('is_available', 'specialization')


@admin.register(AdvisorProfile)
class AdvisorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'branch', 'employee_id')
