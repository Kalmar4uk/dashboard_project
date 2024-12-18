# Generated by Django 4.2 on 2024-10-17 08:41

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('competencies', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='individualdevelopmentplan',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Сотрудник'),
        ),
        migrations.AddField(
            model_name='employeeskills',
            name='appreciated',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='appreciateds', to=settings.AUTH_USER_MODEL, verbose_name='Оценивший'),
        ),
        migrations.AddField(
            model_name='employeeskills',
            name='competence',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='competence', to='competencies.skills', verbose_name='Навык'),
        ),
        migrations.AddField(
            model_name='employeeskills',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_employeeskills', to=settings.AUTH_USER_MODEL, verbose_name='Сотрудник'),
        ),
    ]
