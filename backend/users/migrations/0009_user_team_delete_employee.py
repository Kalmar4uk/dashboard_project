# Generated by Django 4.2 on 2024-10-10 07:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_remove_team_count_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='team',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='users', to='users.team', verbose_name='Команда'),
        ),
        migrations.DeleteModel(
            name='Employee',
        ),
    ]