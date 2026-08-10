"""
ShopSphere — Base Django Settings
Shared settings across development and production environments.
"""

import os
from pathlib import Path
import environ

BASE_DIR = Path(__file__).resolve().parent.parent.parent

env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

SECRET_KEY = env('SECRET_KEY', default='django-insecure-shopsphere-dev-key-change-this-in-production-abc123xyz')

DEBUG = env.bool('DEBUG', default=True)

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['localhost', '127.0.0.1'])

# Application Definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-Party Apps
    # 'cloudinary',
    # 'cloudinary_storage',

    # Local Apps (Modular Structure)
    'core.apps.CoreConfig',
    'accounts.apps.AccountsConfig',
    'products.apps.ProductsConfig',
    'categories.apps.CategoriesConfig',
    'cart.apps.CartConfig',
    'wishlist.apps.WishlistConfig',
    'orders.apps.OrdersConfig',
    'payments.apps.PaymentsConfig',
    'reviews.apps.ReviewsConfig',
    'notifications.apps.NotificationsConfig',
    'dashboard.apps.DashboardConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ecommerce_project.urls'

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
                'cart.context_processors.cart_context',
                'categories.context_processors.categories_processor',
                'wishlist.context_processors.wishlist_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'ecommerce_project.wsgi.application'

# ─── Database ──────────────────────────────────────────────────────────────────
USE_MYSQL = env.bool('USE_MYSQL', default=True)

if not USE_MYSQL:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': env('DB_NAME', default='spcart_db'),
            'USER': env('DB_USER', default='root'),
            'PASSWORD': env('DB_PASSWORD', default=''),
            'HOST': env('DB_HOST', default='127.0.0.1'),
            'PORT': env('DB_PORT', default='3306'),
            'OPTIONS': {
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
                'charset': 'utf8mb4',
            },
        }
    }

# ─── Custom User Model ─────────────────────────────────────────────────────────
AUTH_USER_MODEL = 'accounts.User'

# ─── Password Validation ───────────────────────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ─── Internationalization ──────────────────────────────────────────────────────
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

# ─── Static & Media Files ──────────────────────────────────────────────────────
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# WhiteNoise Storage
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Default Auto Field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ─── Email Configuration (Gmail SMTP Default) ──────────────────────────────────
EMAIL_BACKEND = env('EMAIL_BACKEND', default='django.core.mail.backends.smtp.EmailBackend')
EMAIL_HOST = env('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = env.int('EMAIL_PORT', default=587)
EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS', default=True)
EMAIL_HOST_USER = env('EMAIL_HOST_USER', default='pundsaurav@gmail.com')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL', default='SPCart Support <pundsaurav@gmail.com>')

# ─── Razorpay Payment Gateway Credentials ──────────────────────────────────────
RAZORPAY_KEY_ID = env('RAZORPAY_KEY_ID', default='rzp_test_TO6AddByUy1ngY')
RAZORPAY_KEY_SECRET = env('RAZORPAY_KEY_SECRET', default='x0DmYbAgeblxmKGjvQJDbouM')
