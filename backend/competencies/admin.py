from django.contrib import admin

from .models import Skills, EmployeeSkills, Evaluation, IndividualDevelopmentPlan

admin.site.register(Skills)
admin.site.register(EmployeeSkills)
admin.site.register(Evaluation)
admin.site.register(IndividualDevelopmentPlan)




# from .models import Competence, CompetenceUser, CompetencyAssessment, CompetencyAssessmentUser

# admin.site.register(Competence)
# admin.site.register(CompetencyAssessmentUser)

# @admin.register(CompetenceUser)
# class CompetenceUserAdmin(admin.ModelAdmin):
#     list_display = (
#         'user',
#         'competence',
#         'date_passage'
#     )


# admin.site.register(CompetencyAssessment)
