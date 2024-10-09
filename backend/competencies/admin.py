from django.contrib import admin

from .models import (
    Skills, EmployeeSkills, Evaluation, IndividualDevelopmentPlan
)


@admin.register(EmployeeSkills)
class EmployeeSkillsAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'competence',
        'is_deleted'
    )
    list_filter = (
        'is_deleted',
        'user',
        'competence'
    )
    search_fields = (
        'user',
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

@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    list_display = (
        'employee',
        'value_evaluation',
        'type_evaluation',
        'accordance',
        'appreciated',
        'date_evaluation',
        'is_deleted',
    )
    list_filter = (
        'is_deleted',
        'employee',
    )

admin.site.register(IndividualDevelopmentPlan)
