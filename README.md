# Collect Reviews API

Асинхронный сервис сбора и анализа пользовательских отзывов. Приложение построено на FastAPI и PostgreSQL, использует слойную архитектуру и автоматически применяет миграции Alembic.

## Основные возможности

- Создание отзывов с автоматическим определением тональности
- Фильтрация отзывов по тональности (positive/negative/neutral)
- Защита от дубликатов на уровне БД и бизнес-логики
- Валидация и нормализация текста отзывов
- Автоматические миграции базы данных при старте
- Полное покрытие тестами unit тестами

## Стек

- FastAPI (`async def` контроллеры)
- SQLAlchemy 2.0 с `AsyncSession`
- PostgreSQL + драйвер `asyncpg`
- Alembic для миграций
- Docker/Docker Compose для развёртывания
- Pytest (unit)

## Структура проекта

```
app/
├── api/                 # HTTP-роуты и DI
│   └── v1/reviews.py
├── core/                # Конфигурация, БД, обработчики ошибок
├── models/              # ORM-модели SQLAlchemy
├── repositories/        # Доступ к БД (только SQL-операции)
├── schemas/             # Pydantic-схемы
├── services/            # Бизнес-логика и ошибки домена
└── sentiment.py         # Лексический анализатор тональности
```

Дополнительно:

- `alembic/` – конфигурация и миграции БД
- `tests/` – unit и integration тесты
- `docker/` – entrypoint для контейнера

## Быстрый старт (Docker)

```bash
docker compose up --build
```

Сервис будет доступен по адресу [http://localhost:8000](http://localhost:8000). При старте контейнера автоматически выполняется `alembic upgrade head`.

## Локальный запуск без Docker

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# настройте переменные окружения
cp .env .env.local                  # при необходимости обновите DATABASE_URL
export $(cat .env.local | xargs)    # Linux/macOS

# примените миграции
alembic upgrade head

# старт API
uvicorn app.main:app --reload
```

## Переменные окружения

| Переменная           | Назначение                                         |
| -------------------- | -------------------------------------------------- |
| `DATABASE_URL`       | Строка подключения к PostgreSQL (`postgresql+asyncpg://...`) |
| `DATABASE_ECHO`      | Включить лог SQL (`true/false`)                    |
| `TEST_DATABASE_URL`  | URL тестовой БД (используется в `pytest`)          |

## Миграции

Создание новой миграции:

```bash
alembic revision -m "описание"
```

Применение миграций:

```bash
alembic upgrade head
```

## Тестирование

Для интеграционных тестов требуется доступный PostgreSQL и переменная `TEST_DATABASE_URL`.

```bash
pytest
```

### Запуск тестов в Docker

Если разворачиваете проект через Docker Compose, можно выполнить тесты в отдельном контейнере API:

```bash
docker compose run --rm api pytest -vv
```

Скрипт автоматически стартует Uvicorn только при запуске сервера, поэтому при передаче своей команды вы сразу увидите вывод тестов в терминале. Контейнер будет удалён после завершения прогонки.

## API

Документация Swagger доступна по адресу `/docs`, ReDoc – `/redoc`.

### POST `/api/v1/reviews`

Создать новый отзыв с автоматическим определением тональности.

```bash
curl -X POST http://localhost:8000/api/v1/reviews \
     -H "Content-Type: application/json" \
     -d '{"text": "Очень понравился сервис — всё быстро и удобно!"}'
```

### GET `/api/v1/reviews`

Получить список отзывов. Опционально можно фильтровать по тональности.

```bash
curl "http://localhost:8000/api/v1/reviews?sentiment=positive"
```

### Примеры ответов

```json
{
  "id": 1,
  "text": "Очень понравился сервис — всё быстро и удобно!",
  "sentiment": "positive",
  "created_at": "2024-01-01T12:00:00+00:00"
}
```
