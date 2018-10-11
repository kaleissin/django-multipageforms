import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir))

SECRET_KEY = "a))63yeqrs95i2(j%+l=7p!h^&30gil28(dd@bh2r@!xcrxar#"

MIDDLEWARE_CLASSES = ()

INSTALLED_APPS = [
    'multipageforms',
    'multipageforms.tests',
    'demo.demoapp',
]

DATABASES = {
        'default': {
                    'ENGINE': 'django.db.backends.sqlite3',
                    'NAME': ':memory:',
                }
}

ROOT_URLCONF = 'demo.demoapp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(PROJECT_ROOT, "demo/demoapp/templates")],
        'APP_DIRS': True,
    },
]
