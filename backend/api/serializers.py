from django.shortcuts import get_object_or_404
from rest_framework import serializers
import random

from competencies.models import User, Skills, Evaluation, IndividualDevelopmentPlan
from users.models import Team


class TokenSerializer(serializers.Serializer):
    '''Сериализация для токена.'''
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


class UserAndEmployeeSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    is_deleted = serializers.BooleanField()

    class Meta:
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
            'job_title',
            'grade',
            'date_accession',
            'is_deleted'
        )


class UserSerializer(UserAndEmployeeSerializer):
    '''Сериализатор для пользователей.'''

    class Meta(UserAndEmployeeSerializer.Meta):
        model = User


class EmployeeSerializer(UserAndEmployeeSerializer):
    '''Сериализатор для пользователей.'''
    team = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all())

    class Meta:
        fields = UserAndEmployeeSerializer.Meta.fields + ('team',)
        model = User


class TeamSerializer(serializers.ModelSerializer):
    '''Сериализатор для команд.'''
    stress_level = serializers.SerializerMethodField()
    employee_count = serializers.IntegerField(source='employees.count', read_only=True)

    class Meta:
        fields = (
            'id',
            'name',
            'create_date',
            'stress_level',
            'employee_count',
        )
        model = Team

    def get_stress_level(self, obj):
        return random.randint(1, 5)


class SkillSerializer(serializers.ModelSerializer):
    '''Сериализатор для навыков.'''
    skill_score = serializers.IntegerField()
    is_deleted = serializers.BooleanField()

    class Meta:
        fields = (
            'id',
            'name',
            'domen',
            'skill_score',
            'is_deleted'
        )
        model = Skills


class EvaluationSerializer(serializers.ModelSerializer):
    '''Сериализатор для оценки.'''
    evaluator_id = serializers.IntegerField(source='appreciated.id', read_only=True)
    evaluated_id = serializers.IntegerField(source='employee.id', read_only=True)

    class Meta:
        fields = (
            'id',
            'evaluated_id',
            'date_evaluation',
            'type_evaluation',
            'value_evaluation',
            'comment',
            'evaluator_id',
            'accordance',
        )
        model = Evaluation


class DevelopmentSerializer(serializers.ModelSerializer):
    '''Сериализатор индивидуального плана развития.'''
    employee_id = serializers.IntegerField(source='user.id', read_only=True)

    class Meta:
        fields = (
            'id',
            'employee_id',
            'target',
            'start_date',
            'end_date',
            'status',
        )
        model = IndividualDevelopmentPlan
