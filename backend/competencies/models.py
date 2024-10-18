from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

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
        User,
        on_delete=models.CASCADE,
        verbose_name='Сотрудник',
        related_name='user_employeeskills'
    )
    appreciated = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Оценивший',
        related_name='appreciateds'
    )
    competence = models.ForeignKey(
        Skills,
        on_delete=models.CASCADE,
        verbose_name='Навык',
        related_name='competence'
    )
    date_evaluation = models.DateField('Дата оценки')
    type_evaluation = models.CharField('Тип оценки', max_length=30)
    value_evaluation = models.PositiveSmallIntegerField(
        'Значение оценки',
        validators=(MinValueValidator(1), MaxValueValidator(5)),
    )
    comment = models.TextField('Комментарий оценки', null=True, blank=True)
    accordance = models.BooleanField('Соответствие', null=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Навык сотрудника'
        verbose_name_plural = 'Навыки сотрудников'

    def __str__(self) -> str:
        return f'{self.user} оценен по навыку {self.competence}'


class MinScoreByGrade(models.Model):
    grade = models.CharField('Грейд', max_length=6)
    job_title = models.CharField('Должность', max_length=50)
    competence = models.CharField('Название навыка', max_length=100)
    min_score = models.PositiveSmallIntegerField(
        'Значение оценки'
    )

    class Meta:
        verbose_name = 'Минимальная оценка навыка'
        verbose_name_plural = 'Минимальная оценка навыков'

    def __str__(self):
        return (
            f'Минимальная оценка для должности {self.job_title} '
            f'и грейда {self.grade} по навыку {self.competence}'
        )


class IndividualDevelopmentPlan(models.Model):
    '''Модель индивидуального плана развития.'''
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Сотрудник'
    )
    target = models.CharField('Цель', max_length=50)
    start_date = models.DateField('Дата начала')
    end_date = models.DateField('Дата окончания')
    status = models.CharField('Статус', max_length=15)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'План развития'
        verbose_name_plural = 'Планы развития'

    def __str__(self) -> str:
        return f'{self.user} поставил цель {self.target} до {self.end_date}. Сейчас {self.status}'
