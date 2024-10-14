from django.contrib.auth import get_user_model
from django.db.models import Avg
from rest_framework.decorators import action, api_view, permission_classes
from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import (
    TokenSerializer, SkillSerializer, TeamSerializer,
    DevelopmentSerializer, EmployeeSerializer, EmployeeSkillsSerializer,
    UpdateUserPasswordSerializer, TeamWriteSerializer, UpdateUserTeamSerializer, CreateDeleteUserTeamSerilalizer
)
from competencies.models import User, Skills, IndividualDevelopmentPlan, EmployeeSkills
from .filters import UserInTeamFilter
from users.models import Team


class APIToken(APIView):
    permission_classes = [AllowAny,]

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
            ).update(is_deleted=True)
        if user:
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'errors': 'Пользователя с таким id нет'},
            status=status.HTTP_404_NOT_FOUND)


class EmployViewSet(UserAndEmployViewSet):
    queryset = User.objects.all()
    serializer_class = EmployeeSerializer
    http_method_names = ('get', 'put', 'delete')
    filter_backends = (DjangoFilterBackend,)
    filterset_class = UserInTeamFilter

    @action(url_path='me', detail=False)
    def get_users_info(self, request):
        user = User.objects.get(id=request.user.id)
        serializer = EmployeeSerializer(user, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


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
    serializer_class = SkillSerializer
    http_method_names = ('get', 'post', 'put', 'delete')


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    http_method_names = ('get', 'post', 'put', 'delete')
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name',)

    def get_serializer_class(self):
        if self.request.method == 'get':
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
    http_method_names = ('get', 'post', 'put', 'delete')


class EmployeeSkillsViewSet(viewsets.ModelViewSet):
    queryset = EmployeeSkills.objects.all()
    serializer_class = EmployeeSkillsSerializer
