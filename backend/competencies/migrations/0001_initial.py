# Generated by Django 4.2 on 2024-10-06 20:04

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EmployeeSkills',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('competence_score', models.FloatField(verbose_name='Уровень навыка')),
            ],
        ),
        migrations.CreateModel(
            name='Evaluation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_evaluation', models.DateField(auto_now_add=True, verbose_name='Дата оценки')),
                ('value_evaluation', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)], verbose_name='Значение оценки')),
                ('comment', models.TextField(verbose_name='Комментарий оценки')),
                ('accordance', models.BooleanField(default=False, verbose_name='Соответствие')),
            ],
        ),
        migrations.CreateModel(
            name='IndividualDevelopmentPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('target', models.CharField(max_length=50, verbose_name='Цель')),
                ('start_date', models.DateField(auto_now_add=True, verbose_name='Дата начала')),
                ('end_date', models.DateField(verbose_name='Дата окончания')),
                ('status', models.CharField(max_length=15, verbose_name='Статус')),
            ],
        ),
        migrations.CreateModel(
            name='Skills',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название навыка')),
                ('domen', models.CharField(choices=[('Hard skills', 'Soft skills'), ('Soft skilss', 'Hard skills')], max_length=15, verbose_name='Тип навыка')),
                ('skill_score', models.FloatField(verbose_name='Минимальная оценка навыка')),
            ],
        ),
    ]