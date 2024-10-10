from rest_framework import serializers


def validate_first_and_last_name(data):
    if data.isdigit():
        raise serializers.ValidationError(
            'Имя или Фамилия не может состоять из цифр!'
        )
