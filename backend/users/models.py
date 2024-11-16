from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .manager import CustomUserManager


class User(AbstractUser):
    '''Модель юзера'''
    username = None
    email = models.EmailField(_('email address'), unique=True)
    image = models.ImageField()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Employee(models.Model):
    '''Модель сотрудника'''
    email = models.EmailField(_('email address'), unique=True)
    last_name = models.CharField('Фамилия', max_length=150)
    first_name = models.CharField('Имя', max_length=150)
    job_title = models.CharField('Должность', max_length=50)
    grade = models.CharField('Грейд', max_length=6)
    date_accession = models.DateField('Дата устройства', auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Team(models.Model):
    '''Модель команды.'''
    name = models.CharField('Название команды', max_length=50, unique=True)
    employees = models.ManyToManyField(
        Employee,
        verbose_name='Команда',
        related_name='teams'
    )
    create_date = models.DateTimeField(
        'Дата создания команды', auto_now_add=True
    )
    is_deleted = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Команда'
        verbose_name_plural = 'Команды'
        constraints = (
            models.UniqueConstraint(
                fields=('name',),
                name='unique_name'
            ),
        )

    def __str__(self) -> str:
        return self.name
