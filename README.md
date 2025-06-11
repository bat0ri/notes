# Notes API

Бэкенд-сервис для управления заметками с поддержкой тегов и изображений.

## Возможности

- Создание, чтение, обновление и удаление заметок
- Управление тегами для заметок
- Загрузка и хранение изображений
- Версионирование заметок
- REST API с документацией Swagger/OpenAPI

## Технологии

- Python 3.11+
- FastAPI
- SQLAlchemy
- PostgreSQL
- MinIO (S3-совместимое хранилище)
- Alembic для миграций
- Poetry для управления зависимостями

## Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/yourusername/notes.git
cd notes
```

2. Установите Poetry (если еще не установлен):
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

3. Установите зависимости:
```bash
poetry install
```

4. Создайте файл `.env` на основе `.env.example`:
```bash
cp .env.example .env
```

5. Запустите базу данных и MinIO через Docker:
```bash
docker-compose up -d
```

6. Примените миграции:
```bash
poetry run alembic upgrade head
```

7. Запустите приложение:
```bash
poetry run python run.py
```

## Структура проекта

```
notes/
├── alembic/              # Миграции базы данных
├── app/
│   ├── api/             # API эндпоинты
│   │   └── v1/
│   │       ├── endpoints/
│   │       └── router.py
│   ├── core/            # Основные настройки
│   ├── db/              # Работа с базой данных
│   │   ├── repositories/
│   │   └── session.py
│   ├── models/          # SQLAlchemy модели
│   ├── schemas/         # Pydantic схемы
│   ├── services/        # Бизнес-логика
│   └── storage/         # Работа с хранилищем
├── docs/                # Документация
├── tests/               # Тесты
├── .env.example         # Пример конфигурации
├── docker-compose.yml   # Docker конфигурация
├── pyproject.toml       # Зависимости проекта
└── run.py              # Точка входа
```

## API Документация

После запуска приложения, документация API доступна по следующим URL:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- OpenAPI схема: http://localhost:8000/api/v1/openapi.json

## Основные эндпоинты

### Заметки

- `GET /api/v1/notes` - Получить список заметок
- `POST /api/v1/notes` - Создать заметку
- `GET /api/v1/notes/{note_id}` - Получить заметку по ID
- `PUT /api/v1/notes/{note_id}` - Обновить заметку
- `DELETE /api/v1/notes/{note_id}` - Удалить заметку

### Теги

- `GET /api/v1/tags` - Получить список тегов
- `POST /api/v1/tags` - Создать тег
- `GET /api/v1/tags/{tag_id}` - Получить тег по ID
- `DELETE /api/v1/tags/{tag_id}` - Удалить тег

### Изображения

- `POST /api/v1/images/notes/{note_id}/images` - Загрузить изображение
- `GET /api/v1/images/notes/{note_id}/images` - Получить изображения заметки
- `DELETE /api/v1/images/{image_id}` - Удалить изображение

## Разработка

### Запуск тестов

```bash
poetry run pytest
```

### Создание миграции

```bash
poetry run alembic revision --autogenerate -m "Описание изменений"
```

### Применение миграций

```bash
poetry run alembic upgrade head
```

## Лицензия

MIT
