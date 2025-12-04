# Используем легковесный образ Python
FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем requirements.txt первым для лучшего кеширования
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальные файлы проекта
COPY . .

# Создаем директорию для базы данных
RUN mkdir -p /app/data

# Указываем порт, который будет слушать контейнер
EXPOSE 5000

# Команда для запуска приложения
CMD ["python", "main.py"]