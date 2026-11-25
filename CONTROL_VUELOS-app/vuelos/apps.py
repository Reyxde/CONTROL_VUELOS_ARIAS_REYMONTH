from django.apps import AppConfig
from django.db.models.signals import post_migrate


def _crear_grupos(sender, **kwargs):
    from vuelos.permisos import crear_grupos
    crear_grupos()


class VuelosConfig(AppConfig):
    name = 'vuelos'

    def ready(self):
        post_migrate.connect(_crear_grupos, sender=self)