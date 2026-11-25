"""Grupos, permisos y reglas de propiedad de la aplicación."""
from django.contrib.auth.models import Group, Permission

APP = 'vuelos'
ADMINISTRADORES = 'administradores'
OPERADORES = 'operadores'

TODAS = ['add', 'change', 'delete', 'view']


GRUPOS = {
    ADMINISTRADORES: {
        'aerolinea': TODAS,
        'avion': TODAS,
        'pasajero': TODAS,
        'vuelo': TODAS,
    },
    OPERADORES: {
        'aerolinea': ['view'],
        'avion': ['view'],
        'pasajero': ['view'],
        'vuelo': ['view', 'add', 'change', 'delete'],
    },
}


def crear_grupos():
    """Crea (o actualiza) los grupos con sus permisos. Es idempotente."""
    for nombre, modelos in GRUPOS.items():
        grupo, _ = Group.objects.get_or_create(name=nombre)
        codenames = [f'{accion}_{modelo}'
                     for modelo, acciones in modelos.items()
                     for accion in acciones]
        permisos = Permission.objects.filter(
            content_type__app_label=APP, codename__in=codenames)
        grupo.permissions.set(permisos)


def es_administrador(user):
    return user.is_superuser or user.groups.filter(
        name=ADMINISTRADORES).exists()


def puede_modificar_vuelo(user, vuelo):
    """Regla de propiedad: el administrador toca todo; los demás, solo
    los vuelos que ellos mismos crearon."""
    if not user.is_authenticated:
        return False
    return es_administrador(user) or vuelo.creado_por_id == user.pk
