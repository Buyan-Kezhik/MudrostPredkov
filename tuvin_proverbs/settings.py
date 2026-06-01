import dj_database_url
"""
Настройки Django проекта "Мудрость предков"
Курсовая работа по дисциплине "Основы web-программирования"
Студент: Хомушку Алдынай Анатольевна
Группа: ФИТ_304
Направление: 02.03.02 Фундаментальная информатика и информационные технологии
"""

from pathlib import Path
import os

# =============================================================================
# БАЗОВЫЕ НАСТРОЙКИ ПРОЕКТА
# =============================================================================

# Базовая директория проекта (автоматически определяется)
BASE_DIR = Path(__file__).resolve().parent.parent

# Секретный ключ для криптографической подписи сессий и токенов
# В production нужно заменить на случайную строку и хранить в секрете
SECRET_KEY = 'django-insecure-tuvin-proverbs-coursework-2026-key'

# Режим отладки: True для разработки, False для production
DEBUG = True

# Список разрешённых хостов для безопасности
# В production добавить домен сайта
ALLOWED_HOSTS = ['*']

# =============================================================================
# ПРИЛОЖЕНИЯ DJANGO
# =============================================================================

INSTALLED_APPS = [
    # Стандартные приложения Django
    'django.contrib.admin',      # Админ-панель для управления данными
    'django.contrib.auth',       # Система аутентификации пользователей
    'django.contrib.contenttypes', # Система типов контента
    'django.contrib.sessions',   # Управление сессиями пользователей
    'django.contrib.messages',   # Система сообщений для пользователей
    'django.contrib.staticfiles', # Обработка статических файлов
    
    # Наши собственные приложения
    'accounts',                  # Приложение регистрации и входа пользователей
    'game',                      # Приложение игры с тувинскими пословицами
]

# =============================================================================
# MIDDLEWARE (ОБРАБОТЧИКИ ЗАПРОСОВ)
# =============================================================================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',      # Безопасность
    'django.contrib.sessions.middleware.SessionMiddleware', # Сессии
    'django.middleware.common.CommonMiddleware',          # Общие настройки
    'django.middleware.csrf.CsrfViewMiddleware',          # Защита от CSRF
    'django.contrib.auth.middleware.AuthenticationMiddleware', # Аутентификация
    'django.contrib.messages.middleware.MessageMiddleware',  # Сообщения
    'django.middleware.clickjacking.XFrameOptionsMiddleware', # Защита от clickjacking
]

# Корневой модуль URL-адресов
ROOT_URLCONF = 'tuvin_proverbs.urls'

# =============================================================================
# НАСТРОЙКИ ШАБЛОНОВ (HTML)
# =============================================================================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],  # Дополнительные папки с шаблонами
        'APP_DIRS': True,  # Искать шаблоны в папках приложений
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Модуль WSGI для развёртывания
WSGI_APPLICATION = 'tuvin_proverbs.wsgi.application'

# =============================================================================
# БАЗА ДАННЫХ
# =============================================================================

DATABASES = {
    'default': dj_database_url.config(
        default='postgresql://neondb_owner:npg_PgOTMt2HD6Lf@ep-small-cherry-aqev4t0h-pooler.c-8.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require',
        conn_max_age=600
    )
}

# =============================================================================
# ВАЛИДАЦИЯ ПАРОЛЕЙ
# =============================================================================

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# =============================================================================
# ЛОКАЛИЗАЦИЯ И ИНТЕРНАЦИОНАЛИЗАЦИЯ
# =============================================================================

LANGUAGE_CODE = 'ru-ru'  # Русский язык
TIME_ZONE = 'Asia/Krasnoyarsk'  # Часовой пояс Красноярска (Тува)
USE_I18N = True  # Включить интернационализацию
USE_L10N = True  # Включить локализацию форматов
USE_TZ = True  # Использовать часовые пояса

# =============================================================================
# СТАТИЧЕСКИЕ ФАЙЛЫ (CSS, JS, изображения)
# =============================================================================

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'  # Папка для собранных статических файлов

# =============================================================================
# НАСТРОЙКИ АУТЕНТИФИКАЦИИ
# =============================================================================

LOGIN_URL = 'accounts:login'  # Страница входа
LOGIN_REDIRECT_URL = 'game:home'  # Куда перенаправлять после входа
LOGOUT_REDIRECT_URL = 'accounts:login'  # Куда перенаправлять после выхода

# =============================================================================
# ПРОЧИЕ НАСТРОЙКИ
# =============================================================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Настройки для сообщений
from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.DEBUG: 'debug',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'error',
}