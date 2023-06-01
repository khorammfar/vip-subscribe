import sys

from django.apps import AppConfig


class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'
    def ready(self) -> None:
        if '--worker' in sys.argv:
            import run; exit(run.app.run())
