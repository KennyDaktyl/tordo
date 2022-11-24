from pathlib import Path
import os
import socket

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.environ.get("SECRET_KEY")
DEBUG = True

if socket.gethostname() in [
    "Asus",
    "michalp",
    "DESKTOP-HDDTT8P",
    "michal-asus",
    "michal-optiplex9010",
]:
    DEBUG = True
    CSRF_COOKIE_SECURE = False
    DOMAIN = "127.0.0.1:8000"
    DOMAIN_URL = "http://" + DOMAIN
    DATABASE_NAME = "tordo_dev"
    DATABASE_HOST = "localhost"
    SECURE_SSL_REDIRECT = False
    ALLOWED_HOSTS = [
        "127.0.0.1",
        "localhost",
        "51.75.64.242",
        "tordo.resto-app.pl",
    ]
    # SOCIAL_AUTH_FACEBOOK_KEY = os.environ.get("SOCIAL_AUTH_FACEBOOK_KEY_TEST")
    # SOCIAL_AUTH_FACEBOOK_SECRET = os.environ.get("SOCIAL_AUTH_FACEBOOK_SECRET_TEST")

if socket.gethostname() == "vps-1dc44430":
    DOMAIN = "tordo.resto-app.pl"
    ALLOWED_HOSTS = [
        "tordo.resto-app.pl",
    ]
    DEBUG = False
    DATABASE_NAME = "tordo_dev"
    DATABASE_HOST = "127.0.0.1"
    SECURE_SSL_REDIRECT = False
    SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"
    SESSION_COOKIE_DOMAIN = f".{DOMAIN}"
    SESSION_COOKIE_HTTPONLY = True
    CSRF_COOKIE_DOMAIN = f".{DOMAIN}"
    CSRF_COOKIE_HTTPONLY = True
    CORS_ALLOWED_ORIGINS = [
        "https://tordo.resto-app.pl",
        "https://www.facebook.com/",
        "http://cdn.leafletjs.com/leaflet-0.7.3/leaflet.js",
        "http://cdn.leafletjs.com",
        "https://connect.facebook.net",
    ]
    CSRF_TRUSTED_ORIGINS = [
        "https://tordo.resto-app.pl",
        "http://cdn.leafletjs.com/leaflet-0.7.3/leaflet.js",
        "http://cdn.leafletjs.com",
        "https://www.facebook.com/",
        "https://connect.facebook.net",
    ]
    # SOCIAL_AUTH_FACEBOOK_KEY = os.environ.get("SOCIAL_AUTH_FACEBOOK_KEY")
    # SOCIAL_AUTH_FACEBOOK_SECRET = os.environ.get("SOCIAL_AUTH_FACEBOOK_SECRET")


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'web',
    'compressor',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'tordo.urls'

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.media",
            ],
        },
    },
]

WSGI_APPLICATION = 'tordo.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": {
        "NAME": DATABASE_NAME,
        # "ENGINE": "django.db.backends.postgresql",
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "USER": os.environ.get("DB_USER"),
        "PASSWORD": os.environ.get("DB_PASSWORD"),
        "HOST": DATABASE_HOST,
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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

STATIC_URL = "/static/"
STATIC_ROOT = "static"
SITE_ROOT = os.path.dirname(os.path.realpath(__file__))
STATICFILES_DIRS = (os.path.join(SITE_ROOT, "static/"),)

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "compressor.finders.CompressorFinder",
)

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media/")

COMPRESS_URL = STATIC_URL
COMPRESS_ROOT = STATIC_ROOT
COMPRESS_PRECOMPILERS = (("text/jsx", "third_party.react_compressor.ReactFilter"),)
COMPRESS_DEBUG_TOGGLE = False
COMPRESS_CSS_COMPRESSOR = "compressor.css.CssCompressor"
COMPRESS_JS_COMPRESSOR = "compressor.js.JsCompressor"
COMPRESS_PARSER = "compressor.parser.AutoSelectParser"

LANGUAGE_CODE = "pl"
TIME_ZONE = "Europe/Warsaw"
USE_I18N = True
USE_L10N = True
USE_TZ = False
DATETIME_FORMAT = "Y-m-d H:M:S"
DATE_INPUT_FORMATS = "Y-m-d H:M:S"
