from django.apps import AppConfig


class WebProjectConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'web_project'

    def ready(self):
        import web_project.signals
