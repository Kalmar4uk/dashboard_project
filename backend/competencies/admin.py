from django.contrib import admin

from .models import (
    Skills, EmployeeSkills, Evaluation, IndividualDevelopmentPlan
)

admin.site.register(Skills)
admin.site.register(EmployeeSkills)
admin.site.register(Evaluation)
admin.site.register(IndividualDevelopmentPlan)
