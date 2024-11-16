from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import Team, User, Employee


class EmployeeInlines(admin.TabularInline):
    model = Team.employees.through


class TeamInlines(admin.TabularInline):
    model = Employee.teams.through


@admin.register(User)
class UserAdmin(UserAdmin):
    model = User
    list_display = (
        'email',
        'first_name',
        'last_name',
    )
    fieldsets = (
        (None, {'fields': (
            'email', 'password',
        )}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'image')}),
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
                    'is_superuser',
                    'is_staff',
                    'is_active'
                )
            }
        ),
    )
    ordering = ('id',)
    search_fields = ('email', 'first_name', 'last_name')


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    inlines = (EmployeeInlines,)
    list_display = (
        'name',
        'create_date',
    )
    fieldsets = (
        (None, {'fields': (
            'name', 'create_date'
        )}),)
    readonly_fields = ('create_date',)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    inlines = (TeamInlines,)
    model = Employee
    list_display = (
        'email',
        'first_name',
        'last_name',
        'job_title',
        'date_accession',
    )
    list_filter = ('job_title', 'grade')
    readonly_fields = ('date_accession',)
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('date_accession',)
