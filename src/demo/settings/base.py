import os


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))
SITE_ROOT = os.path.dirname(PROJECT_ROOT)

SECRET_KEY = "a))63yeqrs95i2(j%+l=7p!h^&30gil28(dd@bh2r@!xcrxar#"

MANAGERS = ADMINS = []

SITE_ID = 1

USE_I18N = True
USE_L10N = True

TIME_ZONE = "America/Chicago"
LANGUAGE_CODE = "en-us"

# These are for user-uploaded content.
MEDIA_ROOT = os.path.join(PROJECT_ROOT, "demo-media")
MEDIA_URL = "/media/"

# These are for site static media (e.g. CSS and JS)
# This one is where static content is collected to.
STATIC_ROOT = os.path.join(PROJECT_ROOT, "demo-static")
STATIC_URL = "/static/"
ADMIN_MEDIA_PREFIX = "/static/admin/"
STATICFILES_DIRS = [
    os.path.join(PROJECT_ROOT, "static"),
]
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# Template stuff
TEMPLATE_LOADERS = [
    "django.template.loaders.filesystem.Loader",
    "django.template.loaders.app_directories.Loader",
]

TEMPLATE_DIRS = [
    os.path.join(PROJECT_ROOT, "templates"),
]

ROOT_URLCONF = "demo.urls"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "mail_admins": {
            "level": "ERROR",
            "class": "django.utils.log.AdminEmailHandler",
        },
    },
    "loggers": {
        "django.request": {
            "handlers": ["mail_admins"],
            "level": "ERROR",
            "propagate": True,
        },
    },
}

INSTALLED_APPS = [
    "django.contrib.sessions",
#     "django.contrib.staticfiles",
    "django.contrib.messages",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    'django.contrib.admin',

    'multipageforms',
    'demo.demoapp',
]
ROOT_URLCONF = "demo.urls"

DATABASES = {
        'default': {
                    'ENGINE': 'django.db.backends.sqlite3',
                    'NAME': 'demo.sqlite',
                }
}

MIDDLEWARE_CLASSES = [
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]
