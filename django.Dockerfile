# Базовый образ
FROM python:3.11

RUN mkdir -p /code
WORKDIR /code
# Установка зависимостей
COPY requirements.txt .
RUN pip install -r requirements.txt

# Копируем код приложения
COPY admin/ .
# Настройка переменных окружения
ENV DATABASE_URL=postgres://user:password@db:5432/habr
#ENV PORT=8000

# Команда запуска
CMD ["sh","-c","python manage.py makemigrations && python manage.py migrate && python manage.py loaddata initial_role.json && python manage.py runserver 0.0.0.0:8000"]
