from django.shortcuts import get_object_or_404
from rest_framework import serializers

from competencies.models import User


class TokenSerializer(serializers.Serializer):
    email = serializers.CharField(
        required=True)
    password = serializers.CharField(
        required=True
    )

    class Meta:
        model = User
        fields = ('password', 'email')

    def validate_email(self, data):
        if not User.objects.filter(email=data):
            raise serializers.ValidationError(
                'Введен некорректный email!'
            )
        return data

    def validate(self, data):
        user = get_object_or_404(User, email=data['email'])
        if not user.check_password(data['password']):
            raise serializers.ValidationError(
                'Введен некорректный пароль!'
            )
        return data
