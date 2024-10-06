from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Competence(models.Model):
    '''Компетенции'''
    skills = (('hard skill', 'soft skill'))
    skill = models.CharField('Навык', max_length=100)
    competence = models.CharField('Компетенция', max_length=100)
    domen = models.CharField('Домен', max_length=15, choices=skills)

    def __str__(self) -> str:
        return self.competence


class CompetenceUser(models.Model):
    '''Компетенции сотрудника'''
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Сотрудник')
    competence = models.ForeignKey(Competence, on_delete=models.CASCADE, verbose_name='Компетенция')
    date_passage = models.DateField('Дата прохождения', auto_now_add=True)

    def __str__(self) -> str:
        return f'Комепетенция {self.user}'


class CompetencyAssessment(models.Model):
    '''Оценка компетенций'''
    assessment = models.PositiveSmallIntegerField('Оценка')
    description_assessment = models.CharField('Описание оценки', max_length=10)
    meet = models.BooleanField('Соответствие', default=False)

    def __str__(self) -> str:
        return f'{self.assessment}-{self.description_assessment}'


class CompetencyAssessmentUser(models.Model):
    '''Оценка компетенций сотрудника'''
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Сотрудник')
    competency_assessment = models.ForeignKey(CompetencyAssessment, on_delete=models.CASCADE, verbose_name='Оценка компетенции')

    def __str__(self) -> str:
        return f'Оценка {self.user}'


class Team(models.Model):
    '''Команда'''
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Сотрудник')
    name = models.CharField('Команда', max_length=50)

    def __str__(self) -> str:
        return self.name
