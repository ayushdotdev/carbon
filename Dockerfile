# syntax=docker/dockerfile:1.20
FROM python:3.12.11-alpine3.22 AS base

ENV PYTHONDONTWRITEBYTECODE=1\
    PYTHONUNBUFFERED=1

WORKDIR /carbon

# -- Build Stage --
FROM base as builder

ENV \
  PIP_DEFAULT_TIMEOUT=100 \
  PIP_DISABLE_PIP_VERSION_CHECK=1 \
  PIP_NO_CACHE_DIR=off \
  POETRY_NO_INTERACTION=1 \
  POETRY_CACHE_DIR="/var/cache/pypoetry" \
  POETRY_HOME="/usr/local"

COPY . .

RUN apk update \
    && apk add --no-cache gettext \
    && rm -rf /var/cache/apk/* \
    && pip install poetry \
    && poetry install --no-interaction --no-ansi --no-root --only main \
    && poetry run pybabel compile -d locales \
    && find /carbon/.venv \
        -type d \( -name test -o -name tests \) -exec rm -rf {} + \
    && find /carbon/.venv \
        -type f \( -name "*.pyc" -o -name "*.pyo" \) -delete


