# Generated by Django 4.2 on 2024-10-26 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_remove_user_is_deleted_alter_user_employee'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('last_name', models.CharField(max_length=150, verbose_name='Фамилия')),
                ('first_name', models.CharField(max_length=150, verbose_name='Имя')),
                ('job_title', models.CharField(max_length=50, verbose_name='Должность')),
                ('grade', models.CharField(max_length=6, verbose_name='Грейд')),
                ('date_accession', models.DateField(auto_now_add=True, verbose_name='Дата устройства')),
                ('is_deleted', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Сотрудник',
                'verbose_name_plural': 'Сотрудники',
            },
        ),
        migrations.RemoveField(
            model_name='user',
            name='date_accession',
        ),
        migrations.RemoveField(
            model_name='user',
            name='employee',
        ),
        migrations.RemoveField(
            model_name='user',
            name='grade',
        ),
        migrations.RemoveField(
            model_name='user',
            name='job_title',
        ),
        migrations.AddField(
            model_name='user',
            name='image',
            field=models.ImageField(default=1, upload_to=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='team',
            name='employees',
            field=models.ManyToManyField(related_name='teams', to='users.employee', verbose_name='Команда'),
        ),
    ]