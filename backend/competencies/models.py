from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from .constants import SKILLS
# import uuid
# from users.models import Team, Employee

User = get_user_model()


class Skills(models.Model):
    '''Модель навыка.'''
    name = models.CharField('Название навыка', max_length=100)
    domen = models.CharField('Тип навыка', max_length=15, choices=SKILLS)
    skill_score = models.FloatField('Минимальная оценка навыка')
    # тут минимальная оценка должна тем числом, которое можно минимально указать в модели EmployeeSkills в Уровне навыка

    def __str__(self) -> str:
        return self.name


class EmployeeSkills(models.Model):
    '''Модель навыков сотрудника.'''
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Сотрудник')
    competence = models.ForeignKey(Skills, on_delete=models.CASCADE, verbose_name='Навык')
    competence_score = models.FloatField('Уровень навыка')

    def __str__(self) -> str:
        return f'{self.user} оценен по навыку {self.competence}'


class Evaluation(models.Model):
    '''Модель оценки.'''
    date_evaluation = models.DateField('Дата оценки', auto_now_add=True)
    # type_evaluation Тип оценки? Какой тип поля и зачем оно?
    value_evaluation = models.PositiveSmallIntegerField(
        'Значение оценки',
        validators=(MinValueValidator(1), MaxValueValidator(5)),
    )
    comment = models.TextField('Комментарий оценки',)
    accordance = models.BooleanField('Соответствие', default=False)

    def __str__(self) -> str:
        return f'{self.comment} - {self.value_evaluation}'


class IndividualDevelopmentPlan(models.Model):
    '''Модель индивидуального плана развития.'''
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Сотрудник')
    target = models.CharField('Цель', max_length=50)
    start_date = models.DateField('Дата начала', auto_now_add=True)
    end_date = models.DateField('Дата окончания',)
    status = models.CharField('Статус', max_length=15)






# class Competence(models.Model):
#     '''Компетенции.'''
#     skill = models.CharField('Навык', max_length=100)
#     competence = models.CharField('Компетенция', max_length=100)
#     domen = models.CharField('Домен', max_length=15, choices=SKILLS)

#     def __str__(self) -> str:
#         return self.competence


# class CompetenceUser(models.Model):
#     '''Компетенции сотрудника.'''
#     user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Сотрудник')
#     competence = models.ForeignKey(Competence, on_delete=models.CASCADE, verbose_name='Компетенция')
#     date_passage = models.DateField('Дата прохождения', auto_now_add=True)

#     def __str__(self) -> str:
#         return f'Комепетенция {self.user}'


# class CompetencyAssessment(models.Model):
#     '''Оценка компетенций.'''
#     assessment = models.PositiveSmallIntegerField(
#         'Оценка',
#         validators=(MinValueValidator(1), MaxValueValidator(5)),
#     )
#     description_assessment = models.CharField('Описание оценки', max_length=10)
#     meet = models.BooleanField('Соответствие', default=False)

#     def __str__(self) -> str:
#         return f'{self.assessment}-{self.description_assessment}'


# class CompetencyAssessmentUser(models.Model):
#     '''Оценка компетенций сотрудника.'''
#     user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Сотрудник')
#     competency_assessment = models.ForeignKey(CompetencyAssessment, on_delete=models.CASCADE, verbose_name='Оценка компетенции')

#     def __str__(self) -> str:
#         return f'Оценка {self.user}'
