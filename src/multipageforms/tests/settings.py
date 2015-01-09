SECRET_KEY = "a))63yeqrs95i2(j%+l=7p!h^&30gil28(dd@bh2r@!xcrxar#"

MIDDLEWARE_CLASSES = ()

INSTALLED_APPS = [
    'multipageforms',
    'multipageforms.tests',
]

DATABASES = {
        'default': {
                    'ENGINE': 'django.db.backends.sqlite3',
                    'NAME': ':memory:',
                }
}

