# API Документация

## Общая информация

API использует REST архитектуру и работает с JSON форматом данных. Все эндпоинты доступны по базовому URL: `http://localhost:8000/api/v1`.

### Аутентификация

В текущей версии API аутентификация не реализована. В будущем будет добавлена интеграция с Keycloak.

### Формат ответов

Все ответы API возвращаются в формате JSON. В случае ошибки, возвращается объект с полями:

```json
{
    "detail": "Описание ошибки"
}
```

## Заметки

### Получение списка заметок

```http
GET /notes
```

Параметры запроса:
- `skip` (опционально): количество пропускаемых записей (по умолчанию 0)
- `limit` (опционально): максимальное количество записей (по умолчанию 100)

Ответ:
```json
[
    {
        "id": "string",
        "title": "string",
        "content": "string",
        "created_at": "2024-02-20T12:00:00",
        "updated_at": "2024-02-20T12:00:00",
        "version": 1,
        "tags": [
            {
                "id": "string",
                "name": "string"
            }
        ],
        "images": [
            {
                "id": "string",
                "filename": "string",
                "url": "string",
                "content_type": "string",
                "created_at": "2024-02-20T12:00:00"
            }
        ]
    }
]
```

### Создание заметки

```http
POST /notes
```

Тело запроса:
```json
{
    "title": "string",
    "content": "string",
    "tags": ["string"]
}
```

Ответ: объект заметки (как в списке выше)

### Получение заметки по ID

```http
GET /notes/{note_id}
```

Ответ: объект заметки

### Обновление заметки

```http
PUT /notes/{note_id}
```

Тело запроса:
```json
{
    "title": "string",
    "content": "string",
    "tags": ["string"]
}
```

Ответ: обновленный объект заметки

### Удаление заметки

```http
DELETE /notes/{note_id}
```

Ответ:
```json
{
    "status": "success"
}
```

## Теги

### Получение списка тегов

```http
GET /tags
```

Ответ:
```json
[
    {
        "id": "string",
        "name": "string"
    }
]
```

### Создание тега

```http
POST /tags
```

Тело запроса:
```json
{
    "name": "string"
}
```

Ответ: объект тега

### Получение тега по ID

```http
GET /tags/{tag_id}
```

Ответ: объект тега

### Удаление тега

```http
DELETE /tags/{tag_id}
```

Ответ:
```json
{
    "status": "success"
}
```

## Изображения

### Загрузка изображения

```http
POST /images/notes/{note_id}/images
```

Тело запроса: `multipart/form-data`
- `file`: файл изображения

Ответ:
```json
{
    "id": "string",
    "filename": "string",
    "url": "string",
    "content_type": "string",
    "created_at": "2024-02-20T12:00:00",
    "note_id": "string"
}
```

### Получение изображений заметки

```http
GET /images/notes/{note_id}/images
```

Ответ: массив объектов изображений

### Удаление изображения

```http
DELETE /images/{image_id}
```

Ответ:
```json
{
    "status": "success"
}
```

## Коды ошибок

- `400 Bad Request` - Неверный формат запроса
- `404 Not Found` - Ресурс не найден
- `500 Internal Server Error` - Внутренняя ошибка сервера

## Примеры использования

### Создание заметки с тегами

```bash
curl -X POST "http://localhost:8000/api/v1/notes" \
     -H "Content-Type: application/json" \
     -d '{
           "title": "Моя заметка",
           "content": "Содержание заметки",
           "tags": ["важное", "работа"]
         }'
```

### Загрузка изображения

```bash
curl -X POST "http://localhost:8000/api/v1/images/notes/{note_id}/images" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@/path/to/image.jpg"
```

### Получение заметок по тегу

```bash
curl "http://localhost:8000/api/v1/notes?tag=важное"
``` 