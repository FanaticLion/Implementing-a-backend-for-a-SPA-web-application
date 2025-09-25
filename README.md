# Habit Tracker - Трекер полезных привычек

[![Python](https://img.shields.io/badge/Python-3.13-blue)]()
[![Django](https://img.shields.io/badge/Django-4.2-green)]()
[![DRF](https://img.shields.io/badge/DRF-3.14-red)]()
[![Celery](https://img.shields.io/badge/Celery-5.3-orange)]()

Backend-приложение для трекера полезных привычек с интеграцией Telegram-бота для напоминаний.

## 📋 Функциональность

- ✅ **CRUD операции с привычками** - полное управление привычками
- ✅ **Валидация по бизнес-правилам** - 5 строгих правил валидации
- ✅ **JWT-аутентификация** - безопасный вход и регистрация
- ✅ **Пагинация** - по 5 привычек на страницу
- ✅ **Права доступа** - разделение на личные и публичные привычки
- ✅ **Telegram-напоминания** - демо-режим с возможностью реальной интеграции
- ✅ **Периодические задачи** - Celery Beat для напоминаний
- ✅ **CORS настройки** - готово для фронтенда
- ✅ **Тесты** - покрытие >80%
- ✅ **Документация API** - Swagger/OpenAPI

## 🚀 Быстрый старт

### Предварительные требования

- Python 3.13
- Poetry (менеджер зависимостей)
- Redis (для Celery)
- SQLite (разработка) / PostgreSQL (продакшен)

### Установка и запуск

1. **Клонируйте репозиторий:**

```bash
    git clone <git@github.com:FanaticLion/Implementing-a-backend-for-a-SPA-web-application.git>
cd pythonproject15
#### Установите зависимости:

bash
poetry install
#### Активируйте виртуальное окружение:

bash
poetry shell
#### Настройте переменные окружения (создайте файл .env):

env
SECRET_KEY=ваш-секретный-ключ
DEBUG=True
TELEGRAM_BOT_TOKEN=токен-вашего-бота
####Выполните миграции:

bash
python manage.py migrate
#### Создайте суперпользователя:

bash
python manage.py createsuperuser
####Настройте периодические задачи:

bash
python manage.py setup_reminders
####Запустите сервисы:

bash
# Terminal 1 - Redis
redis-server

# Terminal 2 - Celery worker
celery -A config worker -l info

# Terminal 3 - Celery beat
celery -A config beat -l info

# Terminal 4 - Django сервер
python manage.py runserver
#📚 API Endpoints
##Аутентификация
POST /api/users/register/ - Регистрация пользователя

POST /api/users/login/ - Логин (получение JWT токена)

####Привычки
GET /api/habits/ - Список привычек текущего пользователя

POST /api/habits/ - Создание новой привычки

GET /api/habits/{id}/ - Получение деталей привычки

PUT /api/habits/{id}/ - Обновление привычки

PATCH /api/habits/{id}/ - Частичное обновление

DELETE /api/habits/{id}/ - Удаление привычки

GET /api/habits/public/ - Публичные привычки других пользователей

####Документация
GET /api/schema/ - OpenAPI схема

GET /api/docs/ - Swagger UI документация

###🔧 Модель привычки
python
{
    "user": "Владелец",
    "place": "Место выполнения", 
    "time": "Время выполнения",
    "action": "Действие",
    "is_pleasant": "Признак приятной привычки",
    "related_habit": "Связанная привычка",
    "periodicity": "Периодичность (daily/weekly)",
    "reward": "Вознаграждение",
    "time_to_complete": "Время на выполнение (сек)",
    "is_public": "Публичный доступ"
}
###✅ Бизнес-правила валидации
Нельзя одновременно указывать связанную привычку и вознаграждение

Время выполнения не более 120 секунд

Связанные привычки должны быть приятными

У приятной привычки не может быть вознаграждения или связанной привычки

Периодичность - не реже 1 раза в 7 дней

###🤖 Telegram интеграция
Демо-режим (рекомендуется для тестирования)
Напоминания выводятся в консоль сервера. Не требует настройки Telegram бота.

Реальный режим
Создайте бота через @BotFather

Получите токен и добавьте в .env:

env
TELEGRAM_BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
Бот поддерживает команды:

/start - приветствие и получение chat_id

/help - справка

/myid - показать ваш chat_id

#🧪 Тестирование
bash
# Запуск всех тестов
pytest

# Проверка покрытия
pytest --cov=habits --cov=users --cov-report=html

# Проверка стиля кода
flake8 .

# Сортировка импортов
isort .
        📁 Структура проекта
text
pythonproject15/
├── config/                 # Настройки Django
│   ├── settings/          # Конфигурации (base, dev, prod)
│   └── celery.py          # Конфигурация Celery
├── habits/                # Приложение привычек
│   ├── models.py          # Модель Habit с валидацией
│   ├── views.py           # ViewSet с пагинацией
│   ├── tasks.py           # Celery задачи напоминаний
│   └── tests/             # Полный набор тестов
├── users/                 # Приложение пользователей
│   ├── models.py          # Кастомная модель User
│   └── urls.py            # Эндпоинты аутентификации
├── telegram_bot/          # Интеграция с Telegram
│   ├── bot.py             # Логика бота
│   └── demo_sender.py     # Демо-режим напоминаний
├── .flake8               # Конфигурация линтера
├── pyproject.toml        # Зависимости Poetry
└── README.md            # Документация
🛠 Технологии
Backend: Django 4.2, Django REST Framework 3.14

Аутентификация: JWT (djangorestframework-simplejwt)

Очереди задач: Celery 5.3, Redis 5.0

Документация: drf-spectacular (Swagger)

CORS: django-cors-headers

Переменные окружения: python-dotenv

Тестирование: pytest, pytest-django, coverage

Стиль кода: flake8, isort, black
##👤 Автор
fantastiction - den20020805@gmail.com

##📄 Лицензия
Этот проект создан в учебных целях для курсовой работы.

