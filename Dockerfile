# Этап сборки (build stage)
FROM python:3.11.2-alpine as builder

WORKDIR /code

RUN apk add --no-cache gcc musl-dev libffi-dev python3-dev build-base

ENV POETRY_VERSION=1.7.1
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir poetry==${POETRY_VERSION}

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --only main --no-root

COPY . .

# ---
FROM python:3.11.2-alpine

WORKDIR /code
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY . .

ENV PORT=8000
ENV HOST="0.0.0.0"
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
EXPOSE 8000