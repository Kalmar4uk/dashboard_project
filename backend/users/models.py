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


# class LevelSpeciality(models.Model):
#     user = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         related_name='level',
#         verbose_name='Сотрудник'
#     )
#     name = models.CharField('Название уровня', max_length=50)
#     order_level = models.PositiveSmallIntegerField('Порядок уровня')

#     class Meta:
#         verbose_name = 'Уровень специальности'
#         verbose_name_plural = 'Уровни специальности'

#     def __str__(self) -> str:
#         return self.name
