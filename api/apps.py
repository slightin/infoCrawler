from django.apps import AppConfig

VERBOSE_APP_NAME = "资讯"

class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'
    verbose_name = "api资讯"
