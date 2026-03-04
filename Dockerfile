# syntax=docker/dockerfile:1.20
FROM python:3.12.11-alpine3.22 AS Base

ENV PYTHONDONTWRITEBYTECODE=1\
    PYTHONUNBUFFERED=1

WORKDIR /carbon
