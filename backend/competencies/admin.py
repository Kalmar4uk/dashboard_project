from django.contrib import admin

from .models import (EmployeeSkills, IndividualDevelopmentPlan,
                     MinScoreByGrade, Skills)


@admin.register(EmployeeSkills)
class EmployeeSkillsAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'competence',
        'date_evaluation',
        'is_deleted'
    )
    list_filter = (
        'is_deleted',
        'user',
        'competence'
    )
    search_fields = (
        'user__first_name', 'user__last_name'
    )


@admin.register(Skills)
class SkillsAdmin(admin.ModelAdmin):
    list_filter = (
        'is_deleted',
        'name',
        'domen'
    )
    search_fields = (
        'name',
    )


admin.site.register(IndividualDevelopmentPlan)
admin.site.register(MinScoreByGrade)
