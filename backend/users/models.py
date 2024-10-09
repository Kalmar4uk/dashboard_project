from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .manager import CustomUserManager


class User(AbstractUser):
    '''Модель пользователя'''
    username = None
    email = models.EmailField(_('email address'), unique=True)
    job_title = models.CharField('Должность', max_length=50)
    grade = models.CharField('Грейд', max_length=6)
    date_accession = models.DateField('Дата устройства', auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Team(models.Model):
    '''Модель команды.'''
    name = models.CharField('Название команды', max_length=50)
    create_date = models.DateTimeField(
        'Дата создания команды', auto_now_add=True
    )

    class Meta:
        verbose_name = 'Команда'
        verbose_name_plural = 'Команды'

    def __str__(self) -> str:
        return self.name


class Employee(models.Model):
    '''Модель сотрудника.'''
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, related_name='employees', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

    def __str__(self):
        return f'{self.user} - {self.team}'
