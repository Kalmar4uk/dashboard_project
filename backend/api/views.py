from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken

from .serializers import TokenSerializer
from competencies.models import User


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
