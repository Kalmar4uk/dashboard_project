from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .manager import CustomUserManager


class User(AbstractUser):
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
    create_date = models.DateTimeField('Дата создания команды', auto_now_add=True)

    def __str__(self) -> str:
        return self.name


# по поводу этой модельки стоит еще подумать, наверное, завтра удалю её
class Employee(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} - {self.team}'
