# Базовый образ Python
FROM python:3.10-slim

# Установим переменную окружения для режима, чтобы указать Python не использовать буферизацию (удобно для логов)
ENV PYTHONUNBUFFERED=1

# Установим рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файл с зависимостями (requirements.txt) в контейнер
COPY requirements.txt .

# Установим все зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все файлы проекта в контейнер, включая .env
COPY . .

# Добавляем непользовательские права для безопасности
RUN adduser --disabled-password --gecos '' botuser
USER botuser

# Укажем команду для запуска бота
CMD ["python", "bot.py"]
