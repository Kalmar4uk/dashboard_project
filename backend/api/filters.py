from django_filters import rest_framework as filters

from users.models import User, Team
from competencies.models import EmployeeSkills


class UserInTeamFilter(filters.FilterSet):
    team = filters.ModelChoiceFilter(
        queryset=Team.objects.all(),
        field_name='teams__name',
        to_field_name='name'
    )

    class Meta:
        model = User
        fields = ('team', 'job_title', 'grade')
