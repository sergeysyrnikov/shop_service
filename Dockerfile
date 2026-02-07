# 1. Базовый образ Python
FROM python:3.12-slim

# 2. Системные зависимости (PostgreSQL dev + сборка)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 3. Рабочая директория
WORKDIR /app

# 4. Копируем файлы зависимостей Poetry
COPY pyproject.toml uv.lock* /app/

# 5. Устанавливаем Poetry и зависимости
RUN pip install --no-cache-dir poetry \
    && poetry config virtualenvs.create false \
    && poetry install --without dev --no-root --no-interaction --no-ansi

# 6. Копируем весь проект
COPY . /app

# 7. Логи сразу в stdout
ENV PYTHONUNBUFFERED=1
ENV ENV=dev

# 8. Запуск FastAPI через uvicorn
CMD ["uvicorn", "app.main:shop_app", "--host", "0.0.0.0", "--port", "8000", "--reload"]