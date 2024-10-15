from django_filters import rest_framework as filters

from users.models import Team, User


class UserInTeamFilter(filters.FilterSet):
    team = filters.ModelChoiceFilter(
        queryset=Team.objects.all(),
        field_name='teams__name',
        to_field_name='name'
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'team', 'job_title', 'grade')
