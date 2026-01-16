# Organization Directory API

REST API для справочника организаций, зданий и видов деятельности.
Поддерживает поиск по зданию, названию, виду деятельности (с учетом поддерева)
и по координатам в радиусе.

## Технологии

- Python 3.11
- FastAPI
- SQLAlchemy 2.x (async)
- Alembic
- Pydantic Settings
- PostgreSQL
- Docker / Docker Compose

## Архитектура

- `routers` — HTTP-эндпойнты
- `services` — бизнес-логика
- `repositories` — SQL/ORM-запросы
- `models` — ORM-модели
- `schemas` — Pydantic-схемы
- `db` — база и сессии
- `scripts` — служебные скрипты (seed)

## Конфигурация

Скопируй `.env.example` в `.env` и отредактируй значения:

```bash
cp .env.example .env
```

Переменные:

- `API_KEY` — статический ключ для доступа к API
- `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD` — креды БД

## Запуск в Docker

1) Поднять сервисы:

```bash
docker compose up -d --build
```

2) Применить миграции:

```bash
docker compose run --rm app alembic upgrade head
```

3) Заполнить тестовыми данными:

```bash
docker compose run --rm app python -m app.scripts.seed
```

API будет доступен на `http://localhost:8000`.

Документация:
- Swagger UI: `http://localhost:8000/docs`
- Redoc: `http://localhost:8000/redoc`

## Авторизация

Во всех запросах нужен заголовок `X-API-Key` со значением из `API_KEY`.

## Эндпойнты

### Health

- `GET /health` — проверка сервиса.

### Buildings

- `GET /buildings` — список зданий.

### Organizations

- `GET /organizations/{organization_id}` — карточка организации.
- `GET /organizations?building_id=` — организации в здании.
- `GET /organizations?name=` — поиск по названию (`ILIKE '%query%'`).
- `GET /organizations?activity_id=&include_descendants=true|false` —
  поиск по виду деятельности; по умолчанию `include_descendants=true` и
  включаются все подвиды из дерева.
- `GET /organizations/nearby?latitude=&longitude=&radius_km=` —
  поиск по координатам в радиусе (км).

Правила фильтрации:
- В `GET /organizations` допускается только один фильтр за раз.
- `include_descendants` используется только вместе с `activity_id`.

## Ошибки

Все ошибки возвращаются в формате:

```json
{
  "detail": "Сообщение об ошибке"
}
```

Частые случаи:

- `400 Bad Request` — неверные фильтры (нет фильтра, несколько фильтров, `include_descendants` без `activity_id`).
- `401 Unauthorized` — не передан или неверный `X-API-Key`.
- `404 Not Found` — сущность не найдена (например, `organization`, `building`, `activity`).

## Примеры запросов

```bash
curl -H "X-API-Key: dev-key" "http://localhost:8000/buildings"
```

```bash
curl -H "X-API-Key: dev-key" "http://localhost:8000/organizations?name=milk"
```

```bash
curl -H "X-API-Key: dev-key" \
  "http://localhost:8000/organizations?activity_id=1&include_descendants=true"
```

```bash
curl -H "X-API-Key: dev-key" \
  "http://localhost:8000/organizations/nearby?latitude=55.75&longitude=37.61&radius_km=5"
```
