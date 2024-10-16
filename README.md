Хакатон Dashboard project for Росбанк

### По адресу https://dashboard-hakaton.hopto.org/redoc/ размещена документация к API

В проекте используется:
* python3.11
* Django==4.2
* Django rest framework==3.15.2

### Как запустить проект

*Клонировать репозиторий*
```
https://github.com/Kalmar4uk/dashboard_project.git
```

*Находясь в главной директории проекта создать и активировать виртуальное окружение*
```
python -m venv venv
```

*Обновить pip*
```
python -m pip install --upgrade pip
```

*Установить зависимости*
```
pip install -r requirements.txt
```

* При локальном запуске через ```python manage.py runserver``` необходимо выполнить миграции и прогрузить из файла .csv ингредиенты.
* Так же в проекте есть Dockerfiles каждого модуля (бекенд, фронтенд, нгинкс), открыть Docker Desktop и прописать команду ```docker compose up -d```, после чего выполнить миграции и прогрузить файлы .csv внутри контейнера.

*Перейти в директорию с файлом manage.py, создать и выполнить миграции*
```
python manage.py makemigrations
python manage.py migrate
```

*Перейти в директорию с файлом manage.py и прописать команду*
```
python manage.py import_csv file_name.csv --model_name model
```
Где:
* *file_name.csv* - название файла для загрузки
* *--model_name model* - "--model_name" устанавливается для указания модели, "model" - название модели

* csv-файлы для прогрущки находятся в папке ```backend/data```



