from django.contrib.auth.password_validation import validate_password
from django.db.models import Avg, Q
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from competencies.models import (EmployeeSkills, IndividualDevelopmentPlan,
                                 MinScoreByGrade, Skills, User)
from users.models import Team

from .constants import GRADE, JOB_TITLE, STRESS_LVL_USER
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


class EmployeeSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(
        max_length=150, validators=[validate_first_and_last_name]
    )
    last_name = serializers.CharField(
        max_length=150, validators=[validate_first_and_last_name]
    )
    teams = serializers.StringRelatedField(read_only=True, many=True)
    competence = serializers.SerializerMethodField(read_only=True)
    coef_conformity = serializers.SerializerMethodField(read_only=True)
    stress_level = serializers.SerializerMethodField(read_only=True)

    class Meta:
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
            'job_title',
            'grade',
            'competence',
            'coef_conformity',
            'stress_level',
            'teams',
            'date_accession',
            'employee'
        )
        model = User

    def get_hard_skills(self, user, skill):
        competence = user.user_employeeskills.all()
        avg_skill = competence.filter(
            competence__domen=skill
            ).aggregate(
                Avg('value_evaluation')
                )['value_evaluation__avg']
        return avg_skill

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
        hard_skill = self.get_hard_skills(obj, 'Hard skills')
        soft_skill = self.get_hard_skills(obj, 'Soft skills')
        if hard_skill is None:
            hard_skill = 0
        if soft_skill is None:
            soft_skill = 0
        return {
            'hard_skills': round(hard_skill, 2),
            'soft_skills': round(soft_skill, 2)
        }

    def get_coef_conformity(self, obj):
        user = EmployeeSkills.objects.filter(user=obj)
        accordance_all = user.filter(Q(accordance=True) | Q(accordance=False))
        if not accordance_all:
            return 0
        accordance_true = accordance_all.filter(accordance=True).count()
        return round(accordance_true / accordance_all.count(), 2)

    def get_stress_level(self, obj):
        '''По сотруднику'''
        teams_user = obj.teams.count()
        if teams_user == 0:
            return 0
        stress_lvl = STRESS_LVL_USER[teams_user]
        return stress_lvl


class UserSerializerForTeam(EmployeeSerializer):
    bus_factor = serializers.SerializerMethodField(read_only=True)

    class Meta:
        fields = (
            'id',
            'first_name',
            'last_name',
            'job_title',
            'grade',
            'stress_level',
            'competence',
            'coef_conformity',
            'bus_factor'
        )
        model = User

    def get_bus_factor(self, obj):
        lvl_skills = self.get_competence(obj)
        if lvl_skills.get('hard_skills') >= 4:
            return True
        return False


class TeamSerializer(serializers.ModelSerializer):
    '''Сериализатор для команд.'''
    stress_level = serializers.SerializerMethodField()
    employee_count = serializers.IntegerField(
        source='employees.count',
        read_only=True
    )
    employees = UserSerializerForTeam(many=True)
    average_hard_skills = serializers.SerializerMethodField(read_only=True)
    average_soft_skills = serializers.SerializerMethodField(read_only=True)

    class Meta:
        fields = (
            'id',
            'name',
            'create_date',
            'stress_level',
            'employee_count',
            'average_hard_skills',
            'average_soft_skills',
            'employees',
        )
        model = Team

    def find_users_or_skills_avg(self, obj, competence=None):
        users = obj.employees.all()
        if competence is None:
            return users
        average = []
        for user in users:
            skills = user.user_employeeskills.filter(
                competence__domen=competence
                ).aggregate(
                    Avg(
                        'value_evaluation'
                        )
                    )['value_evaluation__avg']
            if skills is None:
                skills = 0
            average.append(skills)
        result = round(sum(average)/len(average), 2)
        return result

    def get_stress_level(self, obj):
        '''По команде'''
        users = self.find_users_or_skills_avg(obj)
        overall_stress_level = 0
        for user in users:
            overall_stress_level += STRESS_LVL_USER[user.teams.count()]
        return round(overall_stress_level / users.count(), 2)

    def get_average_hard_skills(self, obj):
        competence = 'Hard skills'
        result = self.find_users_or_skills_avg(obj, competence)
        return result

    def get_average_soft_skills(self, obj):
        competence = 'Soft skills'
        result = self.find_users_or_skills_avg(obj, competence)
        return result


class TeamWriteSerializer(serializers.ModelSerializer):
    employees = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), many=True
    )

    class Meta:
        fields = (
            "name",
            "employees"
        )
        model = Team

    def create(self, validated_data):
        employees = validated_data.pop('employees')
        team = Team.objects.create(**validated_data)
        for emoliyee in employees:
            User.objects.filter(id=emoliyee.id).update(team=team)
        return team

    def to_representation(self, instance):
        return TeamSerializer(instance, context={
            'request': self.context.get('request')
        }).data


class UpdateUserTeamSerializer(serializers.Serializer):
    user_in_team = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all()
    )
    new_user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all()
    )

    class Meta:
        fields = (
            'user_in_team',
            'new_user'
        )

    def validate_user_in_team(self, value):
        if not value:
            raise serializers.ValidationError(
                'Необходимо добавить сотрудника на изменение!'
            )
        user = User.objects.get(id=value.id)
        team_id = self.context.get(
            'request'
        ).parser_context.get('kwargs').get('pk')
        team = Team.objects.filter(id=team_id, employees=user)
        if not team:
            raise serializers.ValidationError(
                'Сотрудника нет в команде!'
            )
        return value

    def validate_new_user(self, value):
        if not value:
            raise serializers.ValidationError(
                'Необходимо добавить сотрудника для изменения'
            )
        user = User.objects.get(id=value.id)
        team_id = self.context.get(
            'request'
        ).parser_context.get('kwargs').get('pk')
        team = Team.objects.filter(id=team_id, employees=user)
        if team:
            raise serializers.ValidationError(
                'Сотрудник уже находится в команде!'
            )
        return value

    def to_representation(self, instance):
        return TeamSerializer(instance, context={
            'request': self.context.get('request')
        }).data


class CreateDeleteUserTeamSerilalizer(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all()
    )

    class Meta:
        fields = (
            'user',
        )
        model = Team

    def validate_user(self, value):
        if not value:
            raise serializers.ValidationError(
                'Не передан сотрудник!'
            )
        user = User.objects.get(id=value.id)
        team_id = self.context.get(
            'request'
        ).parser_context.get('kwargs').get('pk')
        team = Team.objects.filter(id=team_id, employees=user)
        if self.context.get('request').method == 'DELETE':
            if not team:
                raise serializers.ValidationError(
                    'Сотрудника нет в команде!'
                )
        if self.context.get('request').method == 'POST':
            if team:
                raise serializers.ValidationError(
                    'Сотрудник уже находится в команде!'
                )
        return value

    def to_representation(self, instance):
        return TeamSerializer(instance, context={
            'request': self.context.get('request')
        }).data


class DevelopmentSerializer(serializers.ModelSerializer):
    '''Сериализатор индивидуального плана развития.'''
    employee = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='user',
    )
    low_skills = serializers.ListField(
        child=serializers.CharField(),
        read_only=True
    )

    class Meta:
        fields = (
            'id',
            'employee',
            'target',
            'start_date',
            'end_date',
            'status',
            'low_skills',
        )
        model = IndividualDevelopmentPlan

    def create(self, validated_data):
        user = validated_data.pop('user')

        employee_skills = EmployeeSkills.objects.filter(
            user=user, is_deleted=False
        )
        min_scores = MinScoreByGrade.objects.all()
        low_skills = set()

        for skill in employee_skills:
            min_score = min_scores.filter(
                competence=skill.competence.name
            ).first()
            if min_score:
                if skill.value_evaluation < min_score.min_score:
                    low_skills.add(skill.competence.name)

        dev_plan = IndividualDevelopmentPlan.objects.create(
            user=user, **validated_data
        )
        dev_plan.save()

        return dev_plan

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        user = instance.user
        employee_skills = EmployeeSkills.objects.filter(
            user=user, is_deleted=False
        )
        min_scores = MinScoreByGrade.objects.all()
        low_skills = set()

        for skill in employee_skills:
            min_score = min_scores.filter(
                competence=skill.competence.name
            ).first()
            if min_score and skill.value_evaluation < min_score.min_score:
                low_skills.add(skill.competence.name)

        representation['low_skills'] = low_skills
        return representation


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
