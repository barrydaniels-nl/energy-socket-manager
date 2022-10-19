from django.apps import AppConfig

class SocketsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'energy.sockets'

    def ready(self):
        from energy.sockets import signals
