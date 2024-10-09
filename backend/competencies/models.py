from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from .constants import SKILLS
from django.utils import timezone
# import uuid
# from users.models import Team, Employee

User = get_user_model()


class Skills(models.Model):
    '''Модель навыка.'''
    name = models.CharField('Название навыка', max_length=100)
    domen = models.CharField('Тип навыка', max_length=15)
    skill_score = models.FloatField('Минимальная оценка навыка', default=1)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Навык'
        verbose_name_plural = 'Навыки'

    def __str__(self) -> str:
        return self.name


class EmployeeSkills(models.Model):
    '''Модель навыков сотрудника.'''
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Сотрудник'
    )
    competence = models.ForeignKey(
        Skills, on_delete=models.CASCADE, verbose_name='Навык'
    )
    competence_score = models.FloatField('Уровень навыка')
    is_deleted = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Навык сотрудника'
        verbose_name_plural = 'Навыки сотрудников'

    def __str__(self) -> str:
        return f'{self.user} оценен по навыку {self.competence}'


class Evaluation(models.Model):
    '''Модель оценки.'''
    employee = models.ForeignKey(
        User, on_delete=models.CASCADE,
        verbose_name='Сотрудник',
        related_name='user'
    )
    appreciated = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Оценивший',
        related_name='appreciated'
    )
    date_evaluation = models.DateField('Дата оценки', auto_now_add=True)
    type_evaluation = models.CharField('Тип оценки', max_length=30)
    value_evaluation = models.PositiveSmallIntegerField(
        'Значение оценки',
        validators=(MinValueValidator(1), MaxValueValidator(5)),
    )
    comment = models.TextField('Комментарий оценки', null=True, blank=True)
    accordance = models.BooleanField('Соответствие', null=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Оценка'
        verbose_name_plural = 'Оценки'

    def __str__(self) -> str:
        return f'Оценка сотрудника {self.employee}'


class IndividualDevelopmentPlan(models.Model):
    '''Модель индивидуального плана развития.'''
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Сотрудник'
    )
    target = models.CharField('Цель', max_length=50)
    start_date = models.DateField('Дата начала', default=timezone.now)
    end_date = models.DateField('Дата окончания',)
    status = models.CharField('Статус', max_length=15)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'План развития'
        verbose_name_plural = 'Планы развития'

    def __str__(self) -> str:
        return f'{self.user} поставил цель {self.target} до {self.end_date}. Сейчас {self.status}'
