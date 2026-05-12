# Labmedia CRM

Полнофункциональная CRM-система для управления клиентами и платежами с real-time дашбордом и аналитикой.

## Стек технологий

- **Backend:** Django 4.2 LTS, Django REST Framework, Django Channels + Daphne
- **Frontend:** Vue 3 (Composition API, `<script setup>`), Vite 5, Pinia, Vue Router
- **База данных:** PostgreSQL 14
- **Real-time:** WebSocket через Channels + Redis
- **Визуализация:** Apache ECharts
- **Инфраструктура:** Docker Compose, Nginx

## Архитектура проекта

```
labmedia-test/
├── backend/
│   ├── apps/
│   │   ├── clients/          # Модель, API, сериализация клиентов
│   │   └── payments/         # Модель, API, WebSocket consumer, сигналы
│   ├── config/               # Настройки Django, ASGI/WSGI, URLs
│   ├── manage.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── api/              # HTTP-клиент (Axios)
│   │   ├── components/       # Таблицы, формы, графики, уведомления
│   │   ├── store/            # Pinia-сторы (clients, payments)
│   │   ├── views/            # Страницы (Dashboard, Clients, Payments)
│   │   ├── router/           # Vue Router
│   │   └── websocket/        # Reconnecting WebSocket-клиент
│   ├── package.json
│   ├── vite.config.js
│   ├── nginx.conf
│   └── Dockerfile
├── docker-compose.yml
├── init.sql
└── .env
```

## Модели данных

### Client
- `id` — первичный ключ
- `first_name` — имя
- `last_name` — фамилия
- `country` — страна (с индексом)

### Payment
- `id` — первичный ключ
- `payer` — внешний ключ на `Client` (с индексом)
- `amount` — сумма платежа
- `percent` — процент (0–100)
- `pay_date` — дата платежа (с индексом по `payer + pay_date`)

## API

REST API доступен по префиксу `/api/`:

| Метод | Endpoint | Описание |
|-------|----------|----------|
| GET / POST | `/api/clients/` | Список / создание клиентов |
| GET / PUT / PATCH / DELETE | `/api/clients/{id}/` | Детали / редактирование / удаление клиента |
| GET / POST | `/api/payments/` | Список / создание платежей |
| GET / PUT / PATCH / DELETE | `/api/payments/{id}/` | Детали / редактирование / удаление платежа |

Поддерживается фильтрация, поиск и пагинация (20 элементов на страницу).

## WebSocket

- **Endpoint:** `ws://localhost:5173/ws/dashboard/` (через Nginx) или `ws://localhost:8000/ws/dashboard/` (напрямую к backend)
- **Группа:** `dashboard_updates`
- **События:** при создании/изменении/удалении клиента или платежа рассылается сообщение `model_update` всем подключённым клиентам для live-обновления UI.

## Требования

- Docker >= 24.0
- Docker Compose >= 2.20

## Установка и запуск

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/maxr0zen/labmedia-test.git
   cd labmedia-test
   ```

2. Создайте файл `.env` (пример минимальной конфигурации):
   ```env
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1,backend
   DB_ENGINE=django.db.backends.postgresql
   DB_NAME=labmedia
   DB_USER=postgres
   DB_PASSWORD=postgres
   DB_HOST=db
   DB_PORT=5432
   CORS_ALLOWED_ORIGINS=http://localhost:5173,http://localhost,http://localhost:80
   REDIS_URL=redis://redis:6379/0
   CHANNEL_LAYER_BACKEND=redis
   ```

3. Запустите проект:
   ```bash
   docker-compose up --build
   ```

4. После успешного старта:
   - **Frontend:** http://localhost:5173
   - **Backend API:** http://localhost:8000/api/
   - **Django Admin:** http://localhost:8000/admin/

5. Заполните базу тестовыми данными:
   ```bash
   docker-compose exec backend python manage.py seed_data
   ```

## Разработка

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Vite-прокси настроен на `localhost:8000` для `/api` и `/ws`, поэтому фронтенд в dev-режиме работает без CORS-проблем.

## Переменные окружения

| Переменная | Описание | Значение по умолчанию |
|------------|----------|----------------------|
| `SECRET_KEY` | Django secret key | `django-insecure-change-me-in-production` |
| `DEBUG` | Режим отладки | `True` |
| `ALLOWED_HOSTS` | Разрешённые хосты | `localhost,127.0.0.1` |
| `DB_*` | Параметры подключения к PostgreSQL | см. `settings.py` |
| `CORS_ALLOWED_ORIGINS` | CORS-origins для фронтенда | `http://localhost:5173,...` |
| `REDIS_URL` | URL подключения к Redis | `redis://redis:6379/0` |
| `CHANNEL_LAYER_BACKEND` | Бэкенд Channels (`redis` или `in-memory`) | `redis` |

## Скриншоты

> _Скриншоты интерфейса можно добавить сюда после запуска проекта._

## Примечания

- Проект не содержит тестов (pytest / vitest) — при необходимости их можно добавить.
- `DEBUG=True` и fallback `SECRET_KEY` подходят только для локальной разработки.
- В `docker-compose.yml` используется healthcheck для PostgreSQL и Redis — backend стартует только после готовности зависимостей.

## Лицензия

MIT
