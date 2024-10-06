from django.contrib import admin

from .models import Competence, CompetenceUser, CompetencyAssessment, CompetencyAssessmentUser, Team

admin.site.register(Competence)
admin.site.register(CompetencyAssessmentUser)

@admin.register(CompetenceUser)
class CompetenceUserAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'competence',
        'date_passage'
    )


admin.site.register(CompetencyAssessment)
admin.site.register(Team)
