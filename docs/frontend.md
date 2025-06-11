# Документация для фронтенд-разработчиков

## Общая информация

API доступно по базовому URL: `http://localhost:8000/api/v1`

Все запросы и ответы используют формат JSON, кроме загрузки файлов (multipart/form-data).

## Основные эндпоинты

### Заметки

#### Получение списка заметок
```typescript
GET /notes

// Параметры запроса
interface QueryParams {
  skip?: number;    // Пропустить N записей (по умолчанию 0)
  limit?: number;   // Максимальное количество записей (по умолчанию 100)
  tag?: string;     // Фильтр по тегу
}

// Ответ
interface Note {
  id: string;
  title: string;
  content: string;
  created_at: string;  // ISO 8601
  updated_at: string;  // ISO 8601
  version: number;
  tags: Tag[];
  images: Image[];
}
```

#### Создание заметки
```typescript
POST /notes

// Тело запроса
interface CreateNoteRequest {
  title: string;
  content: string;
  tags?: string[];  // Массив имен тегов
}

// Ответ: Note
```

#### Получение заметки по ID
```typescript
GET /notes/{note_id}

// Ответ: Note
```

#### Обновление заметки
```typescript
PUT /notes/{note_id}

// Тело запроса
interface UpdateNoteRequest {
  title?: string;
  content?: string;
  tags?: string[];
}

// Ответ: Note
```

#### Удаление заметки
```typescript
DELETE /notes/{note_id}

// Ответ
interface DeleteResponse {
  status: "success";
}
```

### Теги

#### Получение списка тегов
```typescript
GET /tags

// Ответ
interface Tag[] {
  id: string;
  name: string;
}
```

#### Создание тега
```typescript
POST /tags

// Тело запроса
interface CreateTagRequest {
  name: string;
}

// Ответ: Tag
```

#### Получение тега по ID
```typescript
GET /tags/{tag_id}

// Ответ: Tag
```

#### Удаление тега
```typescript
DELETE /tags/{tag_id}

// Ответ
interface DeleteResponse {
  status: "success";
}
```

### Изображения

#### Загрузка изображения
```typescript
POST /images/notes/{note_id}/images

// Тело запроса: FormData
const formData = new FormData();
formData.append('file', fileInput.files[0]);

// Ответ
interface Image {
  id: string;
  filename: string;
  url: string;
  content_type: string;
  created_at: string;
  note_id: string;
}
```

#### Получение изображений заметки
```typescript
GET /images/notes/{note_id}/images

// Ответ: Image[]
```

#### Удаление изображения
```typescript
DELETE /images/{image_id}

// Ответ
interface DeleteResponse {
  status: "success";
}
```

## Примеры использования

### Axios

```typescript
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Получение списка заметок
const getNotes = async (params?: QueryParams) => {
  const response = await api.get('/notes', { params });
  return response.data;
};

// Создание заметки
const createNote = async (note: CreateNoteRequest) => {
  const response = await api.post('/notes', note);
  return response.data;
};

// Загрузка изображения
const uploadImage = async (noteId: string, file: File) => {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await api.post(`/images/notes/${noteId}/images`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};
```

### React Query

```typescript
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';

// Хук для получения заметок
const useNotes = (params?: QueryParams) => {
  return useQuery({
    queryKey: ['notes', params],
    queryFn: () => getNotes(params),
  });
};

// Хук для создания заметки
const useCreateNote = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: createNote,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['notes'] });
    },
  });
};

// Хук для загрузки изображения
const useUploadImage = (noteId: string) => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (file: File) => uploadImage(noteId, file),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['notes', noteId] });
    },
  });
};
```

## Обработка ошибок

Все ошибки возвращаются в формате:

```typescript
interface ApiError {
  detail: string;
}
```

Коды ошибок:
- `400 Bad Request` - Неверный формат запроса
- `404 Not Found` - Ресурс не найден
- `500 Internal Server Error` - Внутренняя ошибка сервера

Пример обработки ошибок:

```typescript
try {
  const response = await api.get('/notes');
  return response.data;
} catch (error) {
  if (axios.isAxiosError(error)) {
    if (error.response?.status === 404) {
      // Обработка ошибки "не найдено"
    } else if (error.response?.status === 400) {
      // Обработка ошибки валидации
    } else {
      // Обработка других ошибок
    }
  }
  throw error;
}
```

## Рекомендации по реализации

1. Используйте React Query для кэширования и управления состоянием
2. Реализуйте оптимистичные обновления для лучшего UX
3. Добавьте индикаторы загрузки и обработку ошибок
4. Используйте TypeScript для типизации
5. Реализуйте пагинацию для списков
6. Добавьте фильтрацию по тегам
7. Реализуйте предпросмотр изображений
8. Добавьте подтверждение для удаления
9. Реализуйте поиск по заметкам
10. Добавьте сортировку заметок

## Типизация

Рекомендуется создать файл с типами:

```typescript
// types/api.ts

export interface Note {
  id: string;
  title: string;
  content: string;
  created_at: string;
  updated_at: string;
  version: number;
  tags: Tag[];
  images: Image[];
}

export interface Tag {
  id: string;
  name: string;
}

export interface Image {
  id: string;
  filename: string;
  url: string;
  content_type: string;
  created_at: string;
  note_id: string;
}

export interface QueryParams {
  skip?: number;
  limit?: number;
  tag?: string;
}

export interface CreateNoteRequest {
  title: string;
  content: string;
  tags?: string[];
}

export interface UpdateNoteRequest {
  title?: string;
  content?: string;
  tags?: string[];
}

export interface CreateTagRequest {
  name: string;
}

export interface DeleteResponse {
  status: "success";
}

export interface ApiError {
  detail: string;
}
``` 