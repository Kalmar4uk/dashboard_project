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

from .serializers import TokenSerializer, UserSerializer, SkillSerializer, TeamSerializer, EvaluationSerializer, DevelopmentSerializer
from competencies.models import User, Skills, Evaluation, IndividualDevelopmentPlan
from users.models import Team, Employee


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


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ('get', 'put', 'delete')


class EmployViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = UserSerializer
    http_method_names = ('get', 'post', 'put', 'delete')


class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skills.objects.all()
    serializer_class = SkillSerializer
    http_method_names = ('get', 'post', 'put', 'delete')


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    http_method_names = ('get', 'post', 'put', 'delete')


class EvaluationViewSet(viewsets.ModelViewSet):
    queryset = Evaluation.objects.all()
    serializer_class = EvaluationSerializer
    http_method_names = ('get', 'post', 'put', 'delete')


class DevelopmentViewSet(viewsets.ModelViewSet):
    queryset = IndividualDevelopmentPlan.objects.all()
    serializer_class = DevelopmentSerializer
    http_method_names = ('get', 'post', 'put', 'delete')
