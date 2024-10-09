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
    domen = models.CharField('Тип навыка', max_length=15, choices=SKILLS)
    # указал дефолтное значение для оценки
    skill_score = models.FloatField('Минимальная оценка навыка', default=1)
    # тут минимальная оценка должна тем числом, которое можно минимально указать в модели EmployeeSkills в Уровне навыка

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
    # Вопрос с Оценившим, кажется, что если оценивший сотрудник
    # уйдет из компании его оценка все равно должна остаться
    # поставил Set_null, можно подумать как прикрутить Set_default
    appreciated = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Оценивший',
        related_name='appreciated'
    )
    date_evaluation = models.DateField('Дата оценки', default=timezone.now)
    type_evaluation = models.CharField('Тип оценки', max_length=15)
    value_evaluation = models.PositiveSmallIntegerField(
        'Значение оценки',
        validators=(MinValueValidator(1), MaxValueValidator(5)),
    )
    comment = models.TextField('Комментарий оценки',)
    accordance = models.BooleanField('Соответствие', default=False)

    class Meta:
        verbose_name = 'Оценка'
        verbose_name_plural = 'Оценки'

    def __str__(self) -> str:
        return f'{self.comment} - {self.value_evaluation}'


class IndividualDevelopmentPlan(models.Model):
    '''Модель индивидуального плана развития.'''
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Сотрудник'
    )
    target = models.CharField('Цель', max_length=50)
    start_date = models.DateField('Дата начала', default=timezone.now)
    end_date = models.DateField('Дата окончания',)
    status = models.CharField('Статус', max_length=15)

    class Meta:
        verbose_name = 'План развития'
        verbose_name_plural = 'Планы развития'

    def __str__(self) -> str:
        return f'{self.user} поставил цель {self.target} до {self.end_date}. Сейчас {self.status}'
