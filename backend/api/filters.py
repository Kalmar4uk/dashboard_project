from django_filters import rest_framework as filters

from users.models import User, Team


class UserInTeamFilter(filters.FilterSet):
    team = filters.ModelMultipleChoiceFilter(
        queryset=Team.objects.all(),
        field_name='team__name',
        to_field_name='name'
    )

    class Meta:
        model = User
        fields = ('team', 'job_title', 'grade')
