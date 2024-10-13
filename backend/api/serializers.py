from django.shortcuts import get_object_or_404
from django.contrib.auth.password_validation import validate_password
from django.db.models import Avg, Sum
from rest_framework import serializers
import random

from competencies.models import User, Skills, IndividualDevelopmentPlan, EmployeeSkills
from users.models import Team

from .constants import GRADE, JOB_TITLE
from .validators import validate_first_and_last_name


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
    first_name = serializers.CharField(
        max_length=150, validators=[validate_first_and_last_name]
    )
    last_name = serializers.CharField(
        max_length=150, validators=[validate_first_and_last_name]
    )
    competence = serializers.SerializerMethodField(read_only=True)
    is_deleted = serializers.BooleanField()

    class Meta:
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
            'job_title',
            'grade',
            'competence',
            'date_accession',
            'is_deleted'
        )

    def validate_grade(self, obj):
        obj = obj.title()
        if obj not in GRADE:
            raise serializers.ValidationError(
                'Нет такого грейда в базе'
            )
        return obj

    def validate_job_title(self, obj):
        obj = obj.title()
        if obj not in JOB_TITLE:
            raise serializers.ValidationError(
                'Нет такой должности в базе'
            )
        return obj

    def get_competence(self, obj):
        competence = obj.user_employeeskills.all()
        serializer = EmployyeSkillsForUserSerializer(competence, many=True)
        return serializer.data


class UserSerializer(UserAndEmployeeSerializer):
    '''Сериализатор для пользователей.'''

    class Meta(UserAndEmployeeSerializer.Meta):
        model = User


class EmployeeSerializer(UserAndEmployeeSerializer):
    '''Сериализатор для пользователей.'''
    password = serializers.CharField(max_length=128, write_only=True)
    team = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all())

    class Meta:
        fields = UserAndEmployeeSerializer.Meta.fields + ('password', 'team')
        model = User

    def validate_password(self, data):
        validate_password(data)
        return data


class UpdateUserPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True)
    current_password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('new_password', 'current_password')

    def validate_current_password(self, data):
        user = self.context['request'].user
        if not user.check_password(data):
            raise serializers.ValidationError(
                'Введен некорректный текущий пароль!'
            )
        return data

    def validate_new_password(self, data):
        validate_password(data)
        return data


class TeamSerializer(serializers.ModelSerializer):
    '''Сериализатор для команд.'''
    stress_level = serializers.SerializerMethodField()
    employee_count = serializers.IntegerField(
        source='users.count',
        read_only=True
    )
    users = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), many=True
    )
    average_hard_skills = serializers.SerializerMethodField(read_only=True)
    average_soft_skills = serializers.SerializerMethodField(read_only=True)
    bus_factor = serializers.SerializerMethodField(read_only=True)

    class Meta:
        fields = (
            'id',
            'name',
            'users',
            'create_date',
            'stress_level',
            'employee_count',
            'average_hard_skills',
            'average_soft_skills',
            'bus_factor'
        )
        model = Team

    def find_users_or_skills_avg(self, obj, competence=None):
        users = obj.users.all()
        if competence is None:
            return users
        average = []
        for user in users:
            average.append(
                user.user_employeeskills.filter(
                    competence__domen=competence
                ).aggregate(
                    Avg(
                        'value_evaluation'
                        )
                    )['value_evaluation__avg']
            )
        result = round(sum(average)/len(average), 2)
        return result

    def get_stress_level(self, obj):
        return random.randint(1, 5)

    def get_average_hard_skills(self, obj):
        competence = 'Hard skills'
        result = self.find_users_or_skills_avg(obj, competence)
        return result

    def get_average_soft_skills(self, obj):
        competence = 'Soft skills'
        result = self.find_users_or_skills_avg(obj, competence)
        return result

    def get_bus_factor(self, obj):
        users = self.find_users_or_skills_avg(obj)
        skill_set = set()
        find_skills = []
        # for user in users:
        #     skills_names = user.user_employeeskills.values('competence__name').filter(competence__domen='Hard skills')
        #     for skill in skills_names:
        #         skill_set.add(skill.get('competence__name'))
        # for skill in skill_set:
        #     for user in users:
        #         skill_user = EmployeeSkills.objects.filter(competence__name=skill)
        #         print(skill_user)
        #         if skill_user:
        #             find_skills.append(skill_user)
        return obj.id


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


class SkillSerializer(serializers.ModelSerializer):
    '''Сериализатор для навыков.'''

    class Meta:
        fields = (
            'id',
            'name',
            'domen',
            'skill_score',
            'is_deleted'
        )
        model = Skills


class EmployeeSkillsSerializer(serializers.ModelSerializer):
    user = EmployeeSerializer()
    appreciated = EmployeeSerializer()
    competence = SkillSerializer()

    class Meta:
        fields = (
            'id',
            'user',
            'appreciated',
            'competence',
            'value_evaluation',
            'type_evaluation',
            'comment',
            'accordance',
            'date_evaluation',
            'is_deleted'
        )
        model = EmployeeSkills


class EmployyeSkillsForUserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            'id',
            'competence',
            'value_evaluation',
            'type_evaluation',
            'accordance'
        )
        model = EmployeeSkills
