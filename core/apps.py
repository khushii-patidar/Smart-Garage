from django.apps import AppConfig
import sys

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        # Clear all sessions on server restart so user is forced to login again!
        if 'runserver' in sys.argv:
            try:
                from django.contrib.sessions.models import Session
                Session.objects.all().delete()
                print("--- ALL SESSIONS CLEARED! Users must log in again. ---")
            except Exception:
                pass
