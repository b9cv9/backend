# Используем официальный образ Python
FROM python:3.11

# Устанавливаем рабочую директорию в контейнере
WORKDIR /code

# Копируем файлы зависимостей
COPY ./requirements.txt /code/requirements.txt

# Устанавливаем зависимости
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Копируем код приложения
COPY ./app /code/app
COPY ./alembic /code/alembic
COPY ./alembic.ini /code/alembic.ini

# Команда для запуска приложения
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]