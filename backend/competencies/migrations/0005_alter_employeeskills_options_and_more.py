# Generated by Django 4.2 on 2024-10-09 13:03

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('competencies', '0004_alter_evaluation_appreciated_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='employeeskills',
            options={'verbose_name': 'Навык сотрудника', 'verbose_name_plural': 'Навыки сотрудников'},
        ),
        migrations.AlterModelOptions(
            name='evaluation',
            options={'verbose_name': 'Оценка', 'verbose_name_plural': 'Оценки'},
        ),
        migrations.AlterModelOptions(
            name='individualdevelopmentplan',
            options={'verbose_name': 'План развития', 'verbose_name_plural': 'Планы развития'},
        ),
        migrations.AlterModelOptions(
            name='skills',
            options={'verbose_name': 'Навык', 'verbose_name_plural': 'Навыки'},
        ),
        migrations.AddField(
            model_name='evaluation',
            name='type_evaluation',
            field=models.CharField(default=django.utils.timezone.now, max_length=15, verbose_name='Тип оценки'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='evaluation',
            name='date_evaluation',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Дата оценки'),
        ),
        migrations.AlterField(
            model_name='individualdevelopmentplan',
            name='start_date',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Дата начала'),
        ),
        migrations.AlterField(
            model_name='skills',
            name='domen',
            field=models.CharField(choices=[('Hard skills', 'Hard skills'), ('Soft skilss', 'Soft skills')], max_length=15, verbose_name='Тип навыка'),
        ),
    ]