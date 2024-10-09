from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User, Team, Employee


class UserInline(admin.TabularInline):
    model = Employee


@admin.register(User)
class UserAdmin(UserAdmin):
    inlines = [UserInline]
    model = User
    list_display = (
        'email',
        'first_name',
        'last_name',
        'job_title',
        'date_accession',
        'is_deleted'
    )
    list_filter = ('is_deleted', 'job_title')
    fieldsets = (
        (None, {'fields': (
            'email', 'password',
        )}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        ('Работа', {'fields': ('grade', 'job_title', 'date_accession')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_superuser', 'is_staff')
            }),
    )
    add_fieldsets = (
        (
            None, {
                'classes': ('wide',),
                'fields': (
                    'email',
                    'password1',
                    'password2',
                    'first_name',
                    'last_name',
                    'job_title',
                    'grade',
                    'is_superuser',
                    'is_staff',
                    'is_active'
                )
            }
        ),
    )
    readonly_fields = ('date_accession',)
    search_fields = ('email',)
    ordering = ('date_accession',)


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'count_user',
        'create_date'
    )
    fieldsets = (
        (None, {'fields': (
            'name', 'count_user', 'create_date'
        )}),)
    readonly_fields = ('create_date', 'count_user')


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'team'
    )
