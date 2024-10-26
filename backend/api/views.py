from datetime import date

from django.db.models import Avg, Q
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from competencies.models import (EmployeeSkills, IndividualDevelopmentPlan,
                                 Skills, User)
from users.models import Team

from .filters import UserInTeamFilter
from .paginations import EmployeePagination
from .permissions import AdminOrReadOnlyPermission
from .serializers import (CreateDeleteUserTeamSerilalizer,
                          DevelopmentSerializer, EmployeeSerializer,
                          EmployeeSkillsSerializer, SkillSerializer,
                          TeamSerializer, TeamWriteSerializer, TokenSerializer,
                          UpdateUserPasswordSerializer,
                          UpdateUserTeamSerializer)


class APIToken(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        user = get_object_or_404(User, email=email)
        refresh = RefreshToken.for_user(user)
        refresh.payload.update(
            {
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name
            }
        )
        return Response(
            {
                'user': {
                    'name': user.first_name + ' ' + user.last_name,
                    'email': user.email
                },
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            },
            status=status.HTTP_201_CREATED
        )


class DeleteAPIToken(APIView):

    def post(self, request):
        refresh_token = request.data.get('refresh_token')
        if not refresh_token:
            return Response(
                {'not_refresh_token': 'Не предоставлен refresh token'},
                status=status.HTTP_400_BAD_REQUEST
            )
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserAndEmployViewSet(viewsets.ModelViewSet):

    def destroy(self, request, *args, **kwargs):
        user = User.objects.filter(
            id=self.kwargs.get('pk')
            ).update(is_active=False)
        if user:
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'errors': 'Пользователя с таким id нет'},
            status=status.HTTP_404_NOT_FOUND)


class EmployViewSet(UserAndEmployViewSet):
    queryset = User.objects.filter(employee=True)
    serializer_class = EmployeeSerializer
    permission_classes = (AdminOrReadOnlyPermission,)
    http_method_names = ('get', 'put', 'delete')
    filter_backends = (DjangoFilterBackend,)
    filterset_class = UserInTeamFilter
    pagination_class = EmployeePagination

    @action(url_path='me', detail=False)
    def get_users_info(self, request):
        user = User.objects.get(id=request.user.id)
        serializer = EmployeeSerializer(user, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(url_path='analytics', detail=True)
    def users_analytics(self, request, pk):
        user = User.objects.get(id=pk)
        analytics = EmployeeSkills.objects.filter(
            user=user
        )
        hard_skills = analytics.filter(competence__domen='Hard skills')
        soft_skills = analytics.filter(competence__domen='Soft skills')
        accordance = analytics.filter(
            Q(accordance=True) | Q(accordance=False)
        )
        hard_skills_one = hard_skills.filter(
            date_evaluation__range=(
                date(2024, 1, 1), date(2024, 3, 30)
            )).aggregate(Avg('value_evaluation'))['value_evaluation__avg']
        hard_skills_two = hard_skills.filter(
            date_evaluation__range=(
                date(2024, 4, 1), date(2024, 6, 30)
            )).aggregate(Avg('value_evaluation'))['value_evaluation__avg']
        hard_skills_three = hard_skills.filter(
            date_evaluation__range=(
                date(2024, 7, 1), date(2024, 9, 30)
            )).aggregate(Avg('value_evaluation'))['value_evaluation__avg']
        hard_skills_four = hard_skills.filter(
            date_evaluation__range=(
                date(2024, 10, 1), date(2024, 12, 31)
            )).aggregate(Avg('value_evaluation'))['value_evaluation__avg']
        soft_skills_one = soft_skills.filter(
            date_evaluation__range=(
                date(2024, 1, 1), date(2024, 3, 30)
            )).aggregate(Avg('value_evaluation'))['value_evaluation__avg']
        soft_skills_two = soft_skills.filter(
            date_evaluation__range=(
                date(2024, 4, 1), date(2024, 6, 30)
            )).aggregate(Avg('value_evaluation'))['value_evaluation__avg']
        soft_skills_three = soft_skills.filter(
            date_evaluation__range=(
                date(2024, 7, 1), date(2024, 9, 30)
            )).aggregate(Avg('value_evaluation'))['value_evaluation__avg']
        soft_skills_four = soft_skills.filter(
            date_evaluation__range=(
                date(2024, 10, 1), date(2024, 12, 31)
            )).aggregate(Avg('value_evaluation'))['value_evaluation__avg']
        accordance_one_all = accordance.filter(
            date_evaluation__range=(
                date(2024, 1, 1), date(2024, 3, 30)
            ))
        accordance_two_all = accordance.filter(
            date_evaluation__range=(
                date(2024, 4, 1), date(2024, 6, 30)
            ))
        accordance_three_all = accordance.filter(
            date_evaluation__range=(
                date(2024, 7, 1), date(2024, 9, 30)
            ))
        accordance_four_all = accordance.filter(
            date_evaluation__range=(
                date(2024, 10, 1), date(2024, 12, 31)
            ))
        try:
            accordance_one = accordance_one_all.filter(
                accordance=True
            ).count() / accordance_one_all.count()
        except Exception:
            accordance_one = None
        try:
            accordance_two = accordance_two_all.filter(
                accordance=True
            ).count() / accordance_two_all.count()
        except Exception:
            accordance_two = None
        try:
            accordance_three = accordance_three_all.filter(
                accordance=True
            ).count() / accordance_three_all.count()
        except Exception:
            accordance_three = None
        try:
            accordance_four = accordance_four_all.filter(
                accordance=True
            ).count() / accordance_four_all.count()
        except Exception:
            accordance_four = None

        return Response(
            {
                'analytics': {
                    'hard_skills': {
                        'hard_skills_one': hard_skills_one,
                        'hard_skills_two': hard_skills_two,
                        'hard_skills_three': hard_skills_three,
                        'hard_skills_four': hard_skills_four
                    },
                    'soft_skills': {
                        'soft_skills_one': soft_skills_one,
                        'soft_skills_two': soft_skills_two,
                        'soft_skills_three': soft_skills_three,
                        'soft_skills_four': soft_skills_four
                    },
                    'accordance': {
                        'accordance_one': accordance_one,
                        'accordance_two': accordance_two,
                        'accordance_three': accordance_three,
                        'accordance_four': accordance_four
                    }
                }
            }
        )


class UpdateUserPassword(APIView):

    def post(self, request):
        serializer = UpdateUserPasswordSerializer(
            context={'request': request}, data=request.data
        )
        self.user = request.user

        if serializer.is_valid():
            self.user.set_password(serializer.data.get('new_password'))
            self.user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skills.objects.all()
    permission_classes = (AdminOrReadOnlyPermission,)
    serializer_class = SkillSerializer
    http_method_names = ('get', 'post', 'put', 'delete')


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = (AdminOrReadOnlyPermission,)
    http_method_names = ('get', 'post', 'put', 'delete')
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name',)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TeamSerializer
        return TeamWriteSerializer

    @action(url_path='update_user', methods=['put'], detail=True)
    def update_user(self, request, pk):
        team = Team.objects.get(id=pk)
        serializer = UpdateUserTeamSerializer(
            team, context={'request': request}, data=request.data
        )
        serializer.is_valid(raise_exception=True)
        user_in_team = serializer.validated_data.get('user_in_team')
        new_user = serializer.validated_data.get('new_user')
        team.employees.remove(user_in_team)
        team.employees.add(new_user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(url_path='create_user', methods=['post'], detail=True)
    def create_user(self, request, pk):
        team = Team.objects.get(id=pk)
        serializer = CreateDeleteUserTeamSerilalizer(
            team, context={'request': request}, data=request.data
        )
        serializer.is_valid(raise_exception=True)
        new_user = serializer.validated_data.get('user')
        team.employees.add(new_user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(url_path='delete_user', methods=['delete'], detail=True)
    def delete_user(self, request, pk):
        team = Team.objects.get(id=pk)
        serializer = CreateDeleteUserTeamSerilalizer(
            team, context={'request': request}, data=request.data
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get('user')
        team.employees.remove(user)
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)


class DevelopmentViewSet(viewsets.ModelViewSet):
    queryset = IndividualDevelopmentPlan.objects.all()
    serializer_class = DevelopmentSerializer
    permission_classes = (AdminOrReadOnlyPermission,)
    http_method_names = ('get', 'post', 'put', 'delete')


class EmployeeSkillsViewSet(viewsets.ModelViewSet):
    queryset = EmployeeSkills.objects.all()
    serializer_class = EmployeeSkillsSerializer
    permission_classes = (AdminOrReadOnlyPermission,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('user', 'appreciated')
