from datetime import timedelta
from pathlib import Path
import environ

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
	DEBUG=(bool, False),
	PRODUCTION=(bool, True),
)
environ.Env.read_env(BASE_DIR / '.env')

DEBUG = env('DEBUG', default=False)
PRODUCTION = env('PRODUCTION', default=True)

SECRET_KEY = env('SECRET_KEY')

ALLOWED_HOSTS = env.list(
	'ALLOWED_HOSTS',
	default=['localhost', '127.0.0.1'] if not PRODUCTION else []
)

INSTALLED_APPS = [
	# Django core
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',

	# Third-party
	'rest_framework',
	'rest_framework_simplejwt.token_blacklist',
	'corsheaders',
	'drf_spectacular',
	'easy_thumbnails',
	'filer',

	# Local apps
	'api',
	'account',
    'store'
]

MIDDLEWARE = [
	'corsheaders.middleware.CorsMiddleware',
	'django.middleware.security.SecurityMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': [BASE_DIR / 'templates'],
		'APP_DIRS': True,
		'OPTIONS': {
			'context_processors': [
				'django.template.context_processors.request',
				'django.contrib.auth.context_processors.auth',
				'django.contrib.messages.context_processors.messages',
			],
		},
	},
]

WSGI_APPLICATION = 'backend.wsgi.application'

# Database
if PRODUCTION:
	DATABASES = {
		'default': {
			'ENGINE': 'django.db.backends.postgresql',
			'NAME': env('DB_NAME'),
			'USER': env('DB_USER'),
			'PASSWORD': env('DB_PASSWORD'),
			'HOST': env('DB_HOST', default='localhost'),
			'PORT': env('DB_PORT', default='5432'),
		}
	}
else:
	DATABASES = {
		'default': {
			'ENGINE': 'django.db.backends.sqlite3',
			'NAME': BASE_DIR / 'db.sqlite3',
		}
	}

AUTH_PASSWORD_VALIDATORS = [
	{'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
	{'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
	{'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
	{'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kathmandu'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
if PRODUCTION:
	STATIC_ROOT = BASE_DIR / 'staticfiles'
else:
	STATICFILES_DIRS = [
		BASE_DIR / 'static/',
	]
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Production Security
if PRODUCTION:
	SECURE_SSL_REDIRECT = True
	SESSION_COOKIE_SECURE = True
	CSRF_COOKIE_SECURE = True
	SECURE_HSTS_SECONDS = 31536000
	SECURE_HSTS_INCLUDE_SUBDOMAINS = True
	SECURE_HSTS_PRELOAD = True
	SECURE_CONTENT_TYPE_NOSNIFF = True
	SECURE_BROWSER_XSS_FILTER = True
	SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'
	SESSION_COOKIE_HTTPONLY = True
	SESSION_COOKIE_SAMESITE = 'Lax'
	SESSION_COOKIE_AGE = 3600
	CSRF_COOKIE_HTTPONLY = False
	CSRF_COOKIE_SAMESITE = 'Lax'
	X_FRAME_OPTIONS = 'DENY'
	SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Django REST Framework
REST_FRAMEWORK = {
	'DEFAULT_PERMISSION_CLASSES': [
		'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
	],
	'DEFAULT_AUTHENTICATION_CLASSES': (
		'rest_framework_simplejwt.authentication.JWTAuthentication',
	),
	'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
	'DEFAULT_THROTTLE_CLASSES': [
		'api.throttles.BurstUserRateThrottle',
		'api.throttles.SustainedUserRateThrottle',
		'api.throttles.BurstAnonRateThrottle',
		'api.throttles.SustainedAnonRateThrottle',
		'rest_framework.throttling.ScopedRateThrottle',
	],
	'DEFAULT_THROTTLE_RATES': {
		'burst_user': '60/minute',
		'sustained_user': '2000/hour',
		'burst_anon': '50/minute',
		'sustained_anon': '1000/hour',
		'login_attempts': '10/minute',
	}

}

# Auth User Model
AUTH_USER_MODEL = 'account.User'

# DRF Spectacular (OpenAPI)
SPECTACULAR_SETTINGS = {
	'TITLE': 'Makeover Me API',
	'VERSION': '1.0.0',
	'SERVE_INCLUDE_SCHEMA': False,
	'SECURITY': [{'BearerAuth': []}],
	'SECURITY_DEFINITIONS': {
		'BearerAuth': {
			'type': 'http',
			'scheme': 'bearer',
			'bearerFormat': 'JWT',
		},
	},
	'SWAGGER_UI_SETTINGS': {
		'persistAuthorization': not PRODUCTION,
	},
	'SORT_OPERATIONS': False,
}

# JWT Configuration
SIMPLE_JWT = {
	'ACCESS_TOKEN_LIFETIME': timedelta(
		minutes=env.int('ACCESS_TOKEN_LIFETIME_MINUTES', default=5)
	),
	'REFRESH_TOKEN_LIFETIME': timedelta(
		days=env.int('REFRESH_TOKEN_LIFETIME_DAYS', default=1)
	),

	'ROTATE_REFRESH_TOKENS': env.bool('ROTATE_REFRESH_TOKENS', default=True),
	'BLACKLIST_AFTER_ROTATION': env.bool('BLACKLIST_AFTER_ROTATION', default=True),
	'UPDATE_LAST_LOGIN': env.bool('UPDATE_LAST_LOGIN', default=True),
	'AUTH_COOKIE': 'token',
	'AUTH_COOKIE_HTTP_ONLY': True,
	'AUTH_COOKIE_SECURE': PRODUCTION,
	'AUTH_COOKIE_SAMESITE': 'Lax',

	'ALGORITHM': 'HS512',
	'SIGNING_KEY': SECRET_KEY,

	'AUTH_HEADER_TYPES': ('Bearer',),
	'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',

	'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
}

# CORS / Frontend
FRONTEND_URL = env('FRONTEND_URL', default='http://localhost:3000')
CORS_ALLOWED_ORIGINS = env.list(
	'CORS_ALLOWED_ORIGINS',
	default=[
		'http://localhost:3000',
		'http://127.0.0.1:3000',
	] if not PRODUCTION else []
)
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_HEADERS = [
	'accept',
	'accept-encoding',
	'authorization',
	'content-type',
	'dnt',
	'origin',
	'user-agent',
	'x-csrftoken',
	'x-requested-with',
]

# Email
if PRODUCTION:
	EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
	EMAIL_HOST = env('EMAIL_HOST')
	EMAIL_PORT = env.int('EMAIL_PORT', default=587)
	EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS', default=True)
	EMAIL_HOST_USER = env('EMAIL_HOST_USER')
	EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
	DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL')
else:
	EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Cache Configuration
CACHES = {
	'default': {
		'BACKEND': 'django_redis.cache.RedisCache',
		'LOCATION': env('REDIS_CACHE_URL'),
		'OPTIONS': {
			'CLIENT_CLASS': 'django_redis.client.DefaultClient',
		},
	}
}

# Celery Configuration
CELERY_BROKER_URL = env('CELERY_BROKER_URL', default=env('REDIS_CACHE_URL'))

# Logging
LOG_DIR = BASE_DIR / 'logs'
LOG_DIR.mkdir(exist_ok=True)
LOGGING = {
	'version': 1,
	'disable_existing_loggers': False,
	'formatters': {
		'verbose': {
			'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
			'style': '{',
		},
	},
	'handlers': {
		'console': {
			'level': 'DEBUG',
			'class': 'logging.StreamHandler',
			'formatter': 'verbose',
		},
		'file': {
			'level': 'INFO',
			'class': 'logging.handlers.RotatingFileHandler',
			'filename': LOG_DIR / 'django.log',
			'maxBytes': 1024 * 1024 * 15,
			'backupCount': 10,
			'formatter': 'verbose',
		},
		'security_file': {
			'level': 'INFO',
			'class': 'logging.handlers.RotatingFileHandler',
			'filename': LOG_DIR / 'security.log',
			'maxBytes': 1024 * 1024 * 15,  # 15MB
			'backupCount': 10,
			'formatter': 'verbose',
		},
	},
	'loggers': {
		'django': {
			'handlers': ['file'] if PRODUCTION else ['console'],
			'level': 'INFO',
			'propagate': False,
		},
		'django.security': {
			'handlers': ['security_file'] if PRODUCTION else ['console'],
			'level': 'INFO',
			'propagate': False,
		},
		'django.request': {
			'handlers': ['file'] if PRODUCTION else ['console'],
			'level': 'ERROR',
			'propagate': False,
		},
	},
}

# Other tokens
EMAIL_CONFIRMATION_TOKEN_MAX_AGE = env.int('EMAIL_CONFIRMATION_TOKEN_MAX_AGE', default=10 * 60)

# CSRF Settings
CSRF_FAILURE_VIEW = 'api.views.csrf_failure'
CSRF_COOKIE_NAME = "csrftoken"
CSRF_COOKIE_HTTPONLY = False
CSRF_COOKIE_SECURE = PRODUCTION
CSRF_COOKIE_SAMESITE = 'Lax'
CSRF_TRUSTED_ORIGINS = env.list('CSRF_TRUSTED_ORIGINS', default=[])


# Filer Settings
# THUMBNAIL_HIGH_RESOLUTION = True
# THUMBNAIL_QUALITY = 85
# THUMBNAIL_PROCESSORS = (
# 	'easy_thumbnails.processors.colorspace',
# 	'easy_thumbnails.processors.autocrop',
# 	'filer.thumbnail_processors.scale_and_crop_with_subject_location',
# 	'easy_thumbnails.processors.filters',
# )
# THUMBNAIL_ALIASES = {
# 	'': {
# 		'admin_thumb': {'size': (100, 100), 'crop': True},
# 		'product_thumb': {'size': (400, 400), 'crop': True},
# 		'featured_large': {'size': (800, 600), 'crop': True},
# 	}
# }