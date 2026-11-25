from django.core.management.base import BaseCommand

from vuelos.permisos import crear_grupos


class Command(BaseCommand):
    help = 'Crea los grupos administradores y operadores con sus permisos.'

    def handle(self, *args, **options):
        crear_grupos()
        self.stdout.write(self.style.SUCCESS('Grupos y permisos creados.'))
