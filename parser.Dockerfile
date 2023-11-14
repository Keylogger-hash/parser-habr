# Базовый образ
FROM python:3.11

RUN mkdir -p /code
WORKDIR /code
# Установка зависимостей
COPY requirements.txt .
RUN pip install -r requirements.txt

# Копируем код приложения
COPY parser/async-parser.py  .
COPY parser/crud.py .
# Настройка переменных окружения
ENV DATABASE_URL=postgres://user:password@db:5432/habr
#ENV PORT=8000

# Команда запуска
CMD ["sh","-c","sleep 15 & python async-parser.py"]
