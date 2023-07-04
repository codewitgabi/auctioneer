from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("SECRET_KEY")

DEBUG = os.environ.get("DEBUG") != "False"

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "10.186.122.216",
    "auctioneer.up.railway.app"
]


# Application definition

INSTALLED_APPS = [
    "jazzmin",
    "channels",
    "whitenoise.runserver_nostatic",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # third party apps 
    
    "rest_framework",
    "cloudvault",
    "email_verification.apps.EmailVerificationConfig",
    
    # custom apps
    
    "account.apps.AccountConfig",
    "auction.apps.AuctionConfig",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR, "templates"],
        'APP_DIRS': True,
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

ASGI_APPLICATION = 'core.asgi.application'

WSGI_APPLICATION = 'core.wsgi.application'


# Database

DATABASES = {
     'default': {
         'ENGINE': "django.db.backends.postgresql",
         'NAME': os.environ.get("DB_NAME"),
         "USER": os.environ.get("DB_USER"),
         "PASSWORD": os.environ.get("DB_PASSWORD"),
         "HOST": os.environ.get("DB_HOST"),
         "PORT": os.environ.get("DB_PORT"),
     }
}


# Password validation

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


# Internationalization

LANGUAGE_CODE = 'en-us'

TIME_ZONE = "Africa/Lagos"

USE_I18N = True

USE_L10N = True

USE_TZ = True

TIME_INPUT_FORMATS = ('%I:%M %p',)
DATE_INPUT_FORMATS = ("%Y-%m-%d",)

# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

#STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Default primary key field type

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


AUTH_USER_MODEL = "account.User"

# email config

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = os.environ.get("EMAIL_PORT")
EMAIL_HOST_USER = os.environ.get("EMAIL_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_PASSWORD")
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = "Auctioneer<no_reply@domain.com>"

LOGIN_URL = "account:signin"
LOGIN_REDIRECT_URL = "auction:home"
LOGOUT_REDIRECT_URL = "account:signin"

# channel layers
CHANNEL_LAYERS = {
	"default": {
		"BACKEND": "channels_redis.core.RedisChannelLayer",
		"CONFIG": {
		"hosts": [os.environ.get("REDIS_HOST", "redis://localhost:6379")]
		}
	}
}

PAYPAL_CLIENT_ID = os.environ.get("PAYPAL_CLIENT_ID")

JAZZMIN_SETTINGS = {
    "site_title": "Auctioneer",
    "site_header": "Auctioneer",
    "site_brand": "Auctioneer",
    "welcome_sign": "Auctioneer Admin Dashboad",
    "user_avatar": "avatar",
    "copyright": "Auctioneer by codewitgabi",
    "show_sidebar": True,
    "navigation_expanded": True,
}

# cloudinary config
CLOUDINARY = {
    'cloud_name': os.environ.get("CLOUDINARY_CLOUD_NAME"),
    'api_key': os.environ.get("CLOUDINARY_API_KEY"),
    'api_secret': os.environ.get("CLOUDINARY_API_SECRET"),
    "secure": True
}

DEFAULT_FILE_STORAGE = "cloudvault.cloud_storage.CloudinaryStorage"

#SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
#SECURE_SSL_REDIRECT = True

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
CSRF_TRUSTED_ORIGINS = [
	"http://localhost",
	"https://auctiooneer.up.railway.app",
]

