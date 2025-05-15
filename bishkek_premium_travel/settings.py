"""
Django settings for bishkek_premium_travel project.
"""

from pathlib import Path
from django.utils.translation import gettext_lazy as _
import os # <-- Добавляем импорт os
import dj_database_url # <-- Добавляем импорт dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# Забираем SECRET_KEY из переменных окружения.
# Для локальной разработки, если ключ не установлен в .env файле,
# можно установить его там или использовать временный запасной ключ ТОЛЬКО при DEBUG=True.
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
if not SECRET_KEY and os.environ.get('DJANGO_DEBUG', 'False').lower() == 'true':
    SECRET_KEY = 'django-insecure-23sx#g7=fg+g3igumh*$zq2=7x&v&i^2ptqr6*n_00$g2*r9mx' # Временный ключ для локальной отладки
elif not SECRET_KEY and os.environ.get('DJANGO_DEBUG', 'False').lower() != 'true':
    raise ValueError("DJANGO_SECRET_KEY не установлен в продакшен окружении!")


# SECURITY WARNING: don't run with debug turned on in production!
# Читаем DEBUG из переменной окружения, по умолчанию False для продакшена
DEBUG = os.environ.get('DJANGO_DEBUG', 'False').lower() == 'true'

ALLOWED_HOSTS_STRING = os.environ.get('DJANGO_ALLOWED_HOSTS')
if ALLOWED_HOSTS_STRING:
    ALLOWED_HOSTS = ALLOWED_HOSTS_STRING.split(',')
elif DEBUG:
    ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
else:
    ALLOWED_HOSTS = [] # В продакшене это должно быть заполнено через переменную окружения


# Application definition

INSTALLED_APPS = [
    'modeltranslation',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'hotels',
    'imagekit',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # <-- Whitenoise для статики
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'bishkek_premium_travel.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
            ],
        },
    },
]

WSGI_APPLICATION = 'bishkek_premium_travel.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

# Используем SQLite по умолчанию, если DATABASE_URL не установлена
default_db_url = f"sqlite:///{BASE_DIR / 'db.sqlite3'}"

DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL', default_db_url),
        conn_max_age=600 # Опционально: время жизни соединения для PostgreSQL
    )
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# --- Настройки Интернационализации ---
LANGUAGE_CODE = 'ru'
TIME_ZONE = 'Asia/Bishkek'
USE_I18N = True
USE_TZ = True

LANGUAGES = [
    ('ru', _('Русский')),
    ('ky', _('Кыргызча')),
    ('en', _('English')),
]

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]
# --- Конец Настроек Интернационализации ---


# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
# Папка, куда `collectstatic` будет собирать все статические файлы для продакшена
STATIC_ROOT = BASE_DIR / 'staticfiles'
# Хранилище для статики, оптимизированное Whitenoise
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
# Дополнительные папки, где Django будет искать статику (для разработки)
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# Media files (User uploaded files)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Login/Logout URLs
LOGIN_URL = 'login'
LOGOUT_REDIRECT_URL = 'home_page'
LOGIN_REDIRECT_URL = 'account_profile'

# CSRF_TRUSTED_ORIGINS (может понадобиться на Railway)
# Если вы будете использовать свой домен, добавьте его сюда
# CSRF_TRUSTED_ORIGINS = ['https://your-railway-app-name.up.railway.app', 'https://www.yourcustomdomain.com']
# Пока можно оставить закомментированным. Если при POST-запросах на Railway будет ошибка CSRF, раскомментируйте и добавьте URL.
