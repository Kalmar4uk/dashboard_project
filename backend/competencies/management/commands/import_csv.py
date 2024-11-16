import csv

from django.conf import settings
from django.core.management.base import BaseCommand

from competencies.models import EmployeeSkills, MinScoreByGrade, Skills
from users.models import Team, Employee

PATH_TO_FILE = f'{settings.BASE_DIR}/data/'

MODELS = {
    'Team': Team,
    'Employee': Employee,
    'Skills': Skills,
    'Employeeskills': EmployeeSkills,
    'Minscore': MinScoreByGrade
}


class Command(BaseCommand):
    '''Команда:'''
    '''python manage.py import_csv имя файла.csv'''
    '''--name_model название модели'''
    help = 'Команда импорта .csv файлов'

    def add_arguments(self, parser):
        parser.add_argument('name_file', type=str, help='Название файла csv')
        parser.add_argument(
            '--name_model',
            type=str,
            help='Название модели для добавления из файла csv'
        )

    def handle(self, *args, **kwargs):
        name_file = kwargs['name_file']
        name_model = kwargs['name_model']
        if name_model:
            name_model = name_model.title()
            model = MODELS[name_model]
            with open(
                f'{PATH_TO_FILE}{name_file}', 'r', encoding='utf-8'
            ) as csvfile:
                reader = csv.DictReader(csvfile)
                model.objects.bulk_create(
                    model(**data) for data in reader
                )
                self.stdout.write(
                    self.style.SUCCESS('Данные из файла загружены')
                )
        else:
            with open(
                f'{PATH_TO_FILE}{name_file}', 'r', encoding='utf-8'
            ) as csvfile:
                reader = csv.reader(csvfile)
                for employee, team in reader:
                    employee = Employee.objects.get(id=employee)
                    team = Team.objects.get(id=team)
                    team.employees.add(employee)
                self.stdout.write(
                    self.style.SUCCESS('Данные из файла загружены')
                )
