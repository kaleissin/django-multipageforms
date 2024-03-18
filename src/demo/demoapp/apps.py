from django.apps import AppConfig


class DemoAppConfig(AppConfig):
    name = 'demo.demoapp'
    verbose_name = 'Demoapp'
    default_auto_field = 'django.db.models.BigAutoField'
