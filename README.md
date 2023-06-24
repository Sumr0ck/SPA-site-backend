# Бэкенд сайта сделанный на Django-DRF

## Для запуска контейнера Docker:

создаем образ `docker build . -t spa-backend`

запускаем контейнер на порту 8000 `docker run -d --rm -p 8000:8000 spa-backend`

запускаем в браузере http://localhost:8000

## Для запуска API нужно:

создать виртуальное окружение `python -m venv venv`

активировать окружение `. /venv/bin/activate`

установить зависимости `pip install -r requirements.txt`

переходим в приложение `cd SPA-site-backend`

проводим миграции бд `./manage.py migrate`

загружаем демонстрационные данные `./manage.py loaddata fixtures/db.json`

запускаем сервер `./manage.py runserver`
