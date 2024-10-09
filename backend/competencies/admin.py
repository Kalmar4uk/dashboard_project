from django.contrib import admin

from .models import (
    Skills, EmployeeSkills, Evaluation, IndividualDevelopmentPlan
)


@admin.register(EmployeeSkills)
class EmployeeSkillsAdmin(admin.ModelAdmin):
    list_filter = (
        'user',
        'competence'
    )
    search_fields = (
        'user',
    )


@admin.register(Skills)
class SkillsAdmin(admin.ModelAdmin):
    list_filter = (
        'name',
        'domen'
    )
    search_fields = (
        'name',
    )


admin.site.register(Evaluation)
admin.site.register(IndividualDevelopmentPlan)
