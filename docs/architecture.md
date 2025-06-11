# Архитектура проекта

## Общий обзор

Notes API - это RESTful сервис для управления заметками, построенный с использованием современных практик разработки и архитектурных паттернов. Проект следует принципам чистой архитектуры и разделения ответственности.

## Архитектурные слои

### 1. API Layer (app/api/)

Отвечает за обработку HTTP-запросов и маршрутизацию. Использует FastAPI для создания эндпоинтов.

```mermaid
graph TD
    A[HTTP Request] --> B[API Endpoints]
    B --> C[Dependencies]
    C --> D[Services]
    D --> E[Repositories]
    E --> F[Database]
```

#### Компоненты:
- `endpoints/` - эндпоинты API
- `deps.py` - зависимости FastAPI
- `router.py` - маршрутизация API

### 2. Service Layer (app/services/)

Содержит бизнес-логику приложения. Каждый сервис отвечает за определенную область функциональности.

```mermaid
graph TD
    A[NoteService] --> B[NoteRepository]
    A --> C[TagRepository]
    A --> D[ImageService]
    D --> E[ImageRepository]
    D --> F[Storage]
```

#### Основные сервисы:
- `NoteService` - управление заметками
- `TagService` - управление тегами
- `ImageService` - управление изображениями

### 3. Repository Layer (app/db/repositories/)

Абстракция над базой данных, реализующая паттерн Repository.

```mermaid
graph TD
    A[BaseRepository] --> B[NoteRepository]
    A --> C[TagRepository]
    A --> D[ImageRepository]
    B --> E[SQLAlchemy]
    C --> E
    D --> E
```

#### Особенности:
- Наследование от `BaseRepository`
- Типизация с помощью Generic
- Асинхронные операции

### 4. Domain Layer (app/models/, app/schemas/)

Определяет основные сущности и их взаимодействие.

```mermaid
erDiagram
    Note ||--o{ Tag : has
    Note ||--o{ Image : contains
    Note ||--o{ NoteVersion : versions
    NoteVersion }|--|| Note : belongs_to
```

#### Модели:
- `Note` - заметка
- `Tag` - тег
- `Image` - изображение
- `NoteVersion` - версия заметки

#### Схемы:
- Pydantic модели для валидации
- Отдельные схемы для создания/обновления/ответа

### 5. Infrastructure Layer (app/storage/, app/core/)

Обеспечивает взаимодействие с внешними системами.

```mermaid
graph TD
    A[MinioStorage] --> B[S3 Client]
    B --> C[MinIO Server]
    D[Database] --> E[PostgreSQL]
    F[Config] --> G[Environment]
```

#### Компоненты:
- `MinioStorage` - работа с MinIO
- `Config` - конфигурация приложения
- `Database` - настройки базы данных

## Асинхронность

Проект использует асинхронное программирование для эффективной обработки запросов:

```mermaid
sequenceDiagram
    participant Client
    participant API
    participant Service
    participant Repository
    participant Database
    
    Client->>API: HTTP Request
    API->>Service: async call
    Service->>Repository: async query
    Repository->>Database: async operation
    Database-->>Repository: result
    Repository-->>Service: result
    Service-->>API: response
    API-->>Client: HTTP Response
```

## Обработка ошибок

```mermaid
graph TD
    A[HTTP Request] --> B{Validation}
    B -->|Invalid| C[400 Bad Request]
    B -->|Valid| D{Business Logic}
    D -->|Error| E[400 Bad Request]
    D -->|Not Found| F[404 Not Found]
    D -->|Success| G[200 OK]
    D -->|Server Error| H[500 Internal Error]
```

## Безопасность

### Аутентификация и авторизация

```mermaid
graph TD
    A[Request] --> B{Has Token}
    B -->|No| C[401 Unauthorized]
    B -->|Yes| D{Valid Token}
    D -->|No| E[403 Forbidden]
    D -->|Yes| F[Process Request]
```

### Защита данных

1. Валидация входных данных
2. Параметризованные запросы
3. Безопасное хранение файлов
4. Логирование действий

## Масштабирование

### Горизонтальное масштабирование

```mermaid
graph TD
    A[Load Balancer] --> B[API Instance 1]
    A --> C[API Instance 2]
    A --> D[API Instance N]
    B --> E[Database]
    C --> E
    D --> E
```

### Стратегии:

1. Репликация базы данных
2. Кэширование
3. Асинхронная обработка
4. Микросервисная архитектура (в будущем)

## Мониторинг

```mermaid
graph TD
    A[Application] --> B[Logging]
    A --> C[Metrics]
    B --> D[ELK Stack]
    C --> E[Prometheus]
    E --> F[Grafana]
```

## Развертывание

### Docker Compose

```mermaid
graph TD
    A[Docker Compose] --> B[API Container]
    A --> C[PostgreSQL Container]
    A --> D[MinIO Container]
    B --> E[Network]
    C --> E
    D --> E
```

### CI/CD Pipeline

```mermaid
graph LR
    A[Git Push] --> B[Tests]
    B --> C[Build]
    C --> D[Deploy]
    D --> E[Production]
```

## Будущие улучшения

1. Микросервисная архитектура
2. Кэширование с Redis
3. Очереди сообщений (RabbitMQ)
4. Сервис поиска (Elasticsearch)
5. Мониторинг и алертинг
6. Контейнеризация с Kubernetes 