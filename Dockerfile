# Используем официальный Python образ в качестве базового
FROM python:3.10-slim

# Устанавливаем зависимости системы для работы с OpenCV
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файл зависимостей
COPY requirements.txt .

# Устанавливаем Python зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все файлы проекта в контейнер
COPY . .

# Устанавливаем переменную окружения для Flask
ENV FLASK_APP=app.py

# Открываем порт для Flask
EXPOSE 5000

# Запускаем приложение
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
