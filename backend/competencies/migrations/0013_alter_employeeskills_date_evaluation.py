# Generated by Django 4.2 on 2024-10-14 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('competencies', '0012_minscorebygrade_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeeskills',
            name='date_evaluation',
            field=models.DateField(verbose_name='Дата оценки'),
        ),
    ]