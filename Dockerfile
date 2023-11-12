# Базовый образ
FROM python:3.11

# Установка зависимостей 
COPY requirements.txt .
RUN pip install -r requirements.txt

# Копируем код приложения
COPY parser/async-parser.py .

# Настройка переменных окружения
ENV DATABASE_URL=postgres://user:password@db:5432/habr
ENV PORT=8000

# Команда запуска
CMD ["python", "async-parser.py"]
