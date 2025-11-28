# Используем официальный образ Python
FROM python:3.13.3-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Копируем файлы зависимостей
COPY pyproject.toml uv.lock alembic.ini ./

# Синхронизируем зависимости с использованием uv
RUN uv sync --frozen --no-dev

# Копируем код приложения
COPY apps/common ./apps/common
COPY apps/gateway ./apps/gateway
COPY apps/__init__.py ./apps/

# Устанавливаем переменные окружения
ENV PYTHONUNBUFFERED=1
ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "apps.gateway.main:app",
    "--host", "0.0.0.0",
    "--port", "8000",
    "--proxy-headers",
    "--forwarded-allow-ips", "[*]",
    "workers", "2"]