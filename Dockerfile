FROM python:3.14-slim AS builder

WORKDIR /app

RUN apt-get update && \
    apt-get install -y git && \
    rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY pyproject.toml uv.lock /app/

ENV UV_LINK_MODE=copy

RUN uv sync --locked --no-install-project --no-editable

FROM python:3.14-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y gdal-bin libgdal-dev binutils libproj-dev && \
    rm -rf /var/lib/apt/lists/*


COPY --from=builder /app/.venv /app/.venv

COPY ./core /app/core
COPY ./manage.py /app/
COPY ./events /app/events

ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1
