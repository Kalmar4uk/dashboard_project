# Generated by Django 4.2 on 2024-10-19 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='employee',
            field=models.BooleanField(default=True, help_text='Отметить, если является этот пользователь сотрудником', verbose_name='Сотрудник'),
        ),
    ]
