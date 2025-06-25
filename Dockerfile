
# builder
FROM python:3.12-bullseye AS builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --no-cache

# runner
FROM python:3.12-slim-bullseye
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
WORKDIR /app

RUN useradd --create-home --shell /bin/bash appuser
USER appuser

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY --from=builder /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"
COPY --chown=appuser:appuser ./src /app/src
EXPOSE 8000

# We use 0.0.0.0 to bind to all network interfaces inside the container
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]