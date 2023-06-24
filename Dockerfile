FROM python:3.8.10
ENV PYTHONUNBUFFERED 1
WORKDIR /app

COPY . .

RUN pip install -r requirements.txt && cd api/ && python manage.py migrate && python manage.py loaddata fixtures/db.json

CMD [ "python", "api/manage.py", "runserver", "0.0.0.0:8000" ]