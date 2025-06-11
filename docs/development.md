# Руководство по разработке

## Настройка окружения разработки

1. Клонируйте репозиторий:
```bash
git clone https://github.com/yourusername/notes.git
cd notes
```

2. Создайте и активируйте виртуальное окружение с помощью Poetry:
```bash
poetry install
poetry shell
```

3. Создайте файл `.env` для разработки:
```bash
cp .env.example .env
```

4. Запустите сервисы через Docker Compose:
```bash
docker-compose up -d
```

## Структура проекта

```
notes/
├── alembic/              # Миграции базы данных
│   ├── versions/        # Файлы миграций
│   ├── env.py          # Настройки окружения Alembic
│   └── script.py.mako  # Шаблон для миграций
├── app/
│   ├── api/            # API эндпоинты
│   │   └── v1/
│   │       ├── endpoints/  # Эндпоинты API
│   │       └── router.py   # Маршрутизация API
│   ├── core/           # Основные настройки
│   │   ├── config.py   # Конфигурация приложения
│   │   └── security.py # Настройки безопасности
│   ├── db/             # Работа с базой данных
│   │   ├── repositories/  # Репозитории для работы с моделями
│   │   └── session.py    # Настройки сессии SQLAlchemy
│   ├── models/         # SQLAlchemy модели
│   ├── schemas/        # Pydantic схемы
│   ├── services/       # Бизнес-логика
│   └── storage/        # Работа с хранилищем
├── docs/               # Документация
├── tests/              # Тесты
│   ├── conftest.py    # Фикстуры pytest
│   └── api/           # Тесты API
├── .env.example       # Пример конфигурации
├── docker-compose.yml # Docker конфигурация
├── pyproject.toml     # Зависимости проекта
└── run.py            # Точка входа
```

## Стиль кода

Проект следует следующим правилам стиля:

1. Используйте [black](https://github.com/psf/black) для форматирования кода:
```bash
poetry run black .
```

2. Проверяйте код с помощью [flake8](https://flake8.pycqa.org/):
```bash
poetry run flake8
```

3. Проверяйте типы с помощью [mypy](https://mypy.readthedocs.io/):
```bash
poetry run mypy .
```

4. Следуйте [PEP 8](https://www.python.org/dev/peps/pep-0008/) и [PEP 484](https://www.python.org/dev/peps/pep-0484/)

## Работа с базой данных

### Создание миграции

1. Внесите изменения в модели в `app/models/`
2. Создайте миграцию:
```bash
poetry run alembic revision --autogenerate -m "Описание изменений"
```

3. Проверьте созданный файл миграции в `alembic/versions/`
4. Примените миграцию:
```bash
poetry run alembic upgrade head
```

### Откат миграции

```bash
poetry run alembic downgrade -1  # Откат на одну версию назад
poetry run alembic downgrade base  # Откат всех миграций
```

## Тестирование

### Запуск тестов

```bash
# Запуск всех тестов
poetry run pytest

# Запуск конкретного теста
poetry run pytest tests/api/test_notes.py

# Запуск с подробным выводом
poetry run pytest -v

# Запуск с выводом print
poetry run pytest -s
```

### Написание тестов

1. Тесты API размещаются в `tests/api/`
2. Используйте фикстуры из `tests/conftest.py`
3. Следуйте структуре:
   - Arrange (подготовка данных)
   - Act (выполнение действия)
   - Assert (проверка результата)

Пример теста:
```python
def test_create_note(client, db_session):
    # Arrange
    note_data = {
        "title": "Test Note",
        "content": "Test Content",
        "tags": ["test"]
    }

    # Act
    response = client.post("/api/v1/notes", json=note_data)

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == note_data["title"]
    assert data["content"] == note_data["content"]
```

## Работа с Git

### Ветки

- `main` - основная ветка, всегда стабильна
- `develop` - ветка разработки
- `feature/*` - ветки для новых функций
- `bugfix/*` - ветки для исправления ошибок
- `hotfix/*` - ветки для срочных исправлений

### Коммиты

Следуйте [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

Типы:
- `feat`: новая функция
- `fix`: исправление ошибки
- `docs`: изменения в документации
- `style`: форматирование кода
- `refactor`: рефакторинг
- `test`: добавление тестов
- `chore`: обновление зависимостей и т.п.

### Pull Request

1. Создайте ветку от `develop`
2. Внесите изменения
3. Напишите тесты
4. Обновите документацию
5. Создайте Pull Request в `develop`
6. Дождитесь проверки кода
7. После мерджа в `develop`, изменения попадут в `main`

## Отладка

### Логирование

Используйте встроенный логгер:

```python
from app.core.logging import logger

logger.info("Информационное сообщение")
logger.error("Сообщение об ошибке", exc_info=True)
```

### Отладка в IDE

1. Настройте конфигурацию запуска в IDE
2. Установите точки останова
3. Запустите приложение в режиме отладки

### Отладка в Docker

```bash
# Просмотр логов
docker-compose logs -f api

# Подключение к контейнеру
docker-compose exec api bash

# Проверка переменных окружения
docker-compose exec api env
```

## Документация

### Обновление документации

1. Обновите docstrings в коде
2. Обновите файлы в `docs/`
3. Проверьте форматирование:
```bash
poetry run black docs/
```

### Генерация документации API

Документация API генерируется автоматически с помощью FastAPI:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## CI/CD

### GitHub Actions

Проект использует GitHub Actions для:
- Проверки стиля кода
- Запуска тестов
- Сборки Docker образов
- Деплоя

### Локальная проверка

```bash
# Запуск всех проверок
poetry run pre-commit run --all-files

# Запуск конкретной проверки
poetry run pre-commit run black --all-files
```

## Производительность

### Профилирование

1. Используйте [cProfile](https://docs.python.org/3/library/profile.html):
```bash
poetry run python -m cProfile -o output.prof run.py
```

2. Анализируйте результаты:
```bash
poetry run snakeviz output.prof
```

### Оптимизация

1. Используйте индексы в базе данных
2. Оптимизируйте запросы
3. Используйте кэширование
4. Минимизируйте количество запросов к базе данных

## Безопасность

### Проверка безопасности

1. Проверяйте зависимости:
```bash
poetry run safety check
```

2. Сканируйте код:
```bash
poetry run bandit -r .
```

### Рекомендации

1. Не храните секреты в коде
2. Используйте параметризованные запросы
3. Валидируйте входные данные
4. Следуйте принципу наименьших привилегий
5. Регулярно обновляйте зависимости 