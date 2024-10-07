from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User, Team, Employee


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = (
        'email',
        'first_name',
        'last_name',
        'job_title',
        'date_accession'
    )
    list_filter = ('job_title',)
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
        'create_date'
    )
    fieldsets = (
        (None, {'fields': (
            'name', 'create_date'
        )}),)
    readonly_fields = ('create_date',)


admin.site.register(Employee)