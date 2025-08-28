FROM python:3.9-slim-bullseye

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    netcat \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Копируем ВЕСЬ проект в /app
WORKDIR /app
COPY project .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt
