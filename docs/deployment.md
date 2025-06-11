# Руководство по развертыванию

## Требования

- Python 3.11 или выше
- Docker и Docker Compose
- Poetry
- PostgreSQL 15 или выше
- MinIO (S3-совместимое хранилище)

## Конфигурация окружения

1. Создайте файл `.env` на основе `.env.example`:

```bash
cp .env.example .env
```

2. Настройте переменные окружения в `.env`:

```env
# Настройки приложения
APP_NAME=Notes API
DEBUG=false
API_V1_STR=/api/v1
PROJECT_HOST=localhost
PROJECT_PORT=8000

# Настройки базы данных
POSTGRES_SERVER=localhost
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=notes
POSTGRES_PORT=5432

# Настройки MinIO
MINIO_ROOT_USER=minioadmin
MINIO_ROOT_PASSWORD=minioadmin
MINIO_URL=localhost:9000
MINIO_BUCKET=notes
MINIO_SECURE=false
```

## Развертывание с помощью Docker Compose

1. Запустите все сервисы:

```bash
docker-compose up -d
```

Это запустит:
- PostgreSQL
- MinIO
- Приложение Notes API

2. Проверьте статус сервисов:

```bash
docker-compose ps
```

3. Примените миграции базы данных:

```bash
docker-compose exec api poetry run alembic upgrade head
```

## Развертывание без Docker

### 1. Установка зависимостей

```bash
# Установка Poetry
curl -sSL https://install.python-poetry.org | python3 -

# Установка зависимостей проекта
poetry install
```

### 2. Настройка базы данных

```bash
# Создание базы данных
createdb notes

# Применение миграций
poetry run alembic upgrade head
```

### 3. Настройка MinIO

1. Скачайте и установите MinIO Server с [официального сайта](https://min.io/download)
2. Запустите MinIO:

```bash
minio server /path/to/data
```

3. Создайте бакет `notes` через веб-интерфейс MinIO (http://localhost:9000)

### 4. Запуск приложения

```bash
poetry run python run.py
```

## Проверка работоспособности

1. Проверьте доступность API:
```bash
curl http://localhost:8000/api/v1/health
```

2. Проверьте документацию API:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Мониторинг

### Логи

```bash
# Просмотр логов всех сервисов
docker-compose logs -f

# Просмотр логов конкретного сервиса
docker-compose logs -f api
```

### Метрики

В будущем будет добавлена интеграция с Prometheus и Grafana для мониторинга.

## Резервное копирование

### База данных

```bash
# Создание бэкапа
docker-compose exec postgres pg_dump -U postgres notes > backup.sql

# Восстановление из бэкапа
docker-compose exec -T postgres psql -U postgres notes < backup.sql
```

### MinIO

Для резервного копирования данных MinIO используйте инструмент `mc`:

```bash
# Установка mc
wget https://dl.min.io/client/mc/release/linux-amd64/mc
chmod +x mc

# Настройка
./mc alias set myminio http://localhost:9000 minioadmin minioadmin

# Копирование данных
./mc mirror myminio/notes /path/to/backup
```

## Обновление

1. Остановите сервисы:
```bash
docker-compose down
```

2. Обновите код:
```bash
git pull origin main
```

3. Пересоберите и запустите сервисы:
```bash
docker-compose up -d --build
```

4. Примените миграции:
```bash
docker-compose exec api poetry run alembic upgrade head
```

## Устранение неполадок

### Проблемы с базой данных

1. Проверьте подключение:
```bash
docker-compose exec postgres psql -U postgres -d notes -c "\l"
```

2. Проверьте логи:
```bash
docker-compose logs postgres
```

### Проблемы с MinIO

1. Проверьте доступность:
```bash
curl http://localhost:9000/minio/health/live
```

2. Проверьте логи:
```bash
docker-compose logs minio
```

### Проблемы с приложением

1. Проверьте логи:
```bash
docker-compose logs api
```

2. Проверьте статус:
```bash
curl http://localhost:8000/api/v1/health
```

## Безопасность

### Рекомендации по безопасности

1. Измените пароли по умолчанию в `.env`
2. Настройте SSL/TLS для API и MinIO
3. Ограничьте доступ к API с помощью брандмауэра
4. Регулярно обновляйте зависимости
5. Используйте секреты для хранения чувствительных данных

### Обновление зависимостей

```bash
# Проверка устаревших пакетов
poetry show --outdated

# Обновление зависимостей
poetry update
``` 