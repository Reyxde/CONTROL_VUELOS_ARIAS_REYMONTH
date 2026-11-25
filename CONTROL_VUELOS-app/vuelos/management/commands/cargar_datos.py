from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.utils import timezone

from vuelos.models import Aerolinea, Avion, Pasajero, Vuelo
from vuelos.permisos import ADMINISTRADORES, OPERADORES

User = get_user_model()

AEROLINEAS = [
    ('Avianca', 'AV', 'Colombia'),
    ('LATAM Airlines', 'LA', 'Chile'),
    ('Copa Airlines', 'CM', 'Panamá'),
    ('Iberia', 'IB', 'España'),
    ('American Airlines', 'AA', 'Estados Unidos'),
]

AVIONES = [  # matrícula, modelo, capacidad, fabricación, estado, IATA
    ('HC-AVA', 'Airbus A320', 180, date(2016, 3, 14), 'OPE', 'AV'),
    ('HC-LAT', 'Boeing 787-9', 290, date(2018, 7, 2), 'OPE', 'LA'),
    ('HC-COP', 'Boeing 737-800', 160, date(2014, 11, 20), 'OPE', 'CM'),
    ('HC-IBE', 'Airbus A330', 250, date(2012, 5, 9), 'MAN', 'IB'),
    ('HC-AAL', 'Boeing 777-200', 300, date(2010, 1, 25), 'OPE', 'AA'),
    ('HC-AVB', 'Embraer E190', 100, date(2019, 9, 30), 'FUE', 'AV'),
]

PASAJEROS = [  # nombre, apellido, documento, nacionalidad, nacimiento
    ('María', 'Andrade', '0912345678', 'Ecuatoriana', date(1990, 4, 12)),
    ('Carlos', 'Mendoza', '0923456789', 'Ecuatoriana', date(1985, 8, 3)),
    ('Laura', 'García', 'X1234567', 'Española', date(1992, 11, 27)),
    ('John', 'Smith', 'US99887766', 'Estadounidense', date(1978, 2, 15)),
    ('Valentina', 'Rojas', 'CO55443322', 'Colombiana', date(2000, 6, 30)),
    ('Pedro', 'Salazar', '0934567890', 'Ecuatoriana', date(1969, 12, 1)),
    ('Ana', 'Pérez', 'PA11223344', 'Panameña', date(1995, 9, 9)),
]

USUARIOS = [  # usuario, clave, grupo (None = superusuario)
    ('admin', 'Admin2026!', None),
    ('jefe_vuelos', 'Jefe2026!', ADMINISTRADORES),
    ('operador1', 'Operador2026!', OPERADORES),
    ('operador2', 'Operador2026!', OPERADORES),
]


class Command(BaseCommand):
    help = 'Carga aerolíneas, aviones, pasajeros, vuelos y usuarios de prueba.'

    def handle(self, *args, **options):
        call_command('crear_grupos', verbosity=0)
        usuarios = self._usuarios()
        aerolineas = {}
        for nombre, iata, pais in AEROLINEAS:
            aerolineas[iata], _ = Aerolinea.objects.update_or_create(
                codigo=iata, defaults={'nombre': nombre, 'pais': pais})
        aviones = []
        for mat, modelo, cap, fab, estado, iata in AVIONES:
            obj, _ = Avion.objects.update_or_create(
                matricula=mat, defaults={
                    'modelo': modelo, 'capacidad': cap,
                    'fecha_fabricacion': fab, 'estado': estado,
                    'aerolinea': aerolineas[iata]})
            aviones.append(obj)
        pasajeros = []
        for nom, ape, doc, nac, nacim in PASAJEROS:
            obj, _ = Pasajero.objects.update_or_create(
                documento=doc, defaults={
                    'nombre': nom, 'apellido': ape, 'nacionalidad': nac,
                    'fecha_nacimiento': nacim})
            pasajeros.append(obj)

        ahora = timezone.now().replace(minute=0, second=0, microsecond=0)
        vuelos = [  # código, origen, destino, +h salida, duración h, estado,
                    # puerta, precio, avion, creador, pasajeros
            ('AV101', 'Guayaquil', 'Bogotá', 3, 2, 'PRO', 'A1', '189.90', 0, 'operador1', [0, 1]),
            ('LA2045', 'Quito', 'Santiago', 5, 5, 'EMB', 'B3', '420.00', 1, 'operador1', [2, 3, 4]),
            ('CM330', 'Guayaquil', 'Panamá', 8, 3, 'PRO', 'A4', '265.50', 2, 'operador2', [5, 6]),
            ('AA907', 'Guayaquil', 'Miami', 12, 4, 'PRO', 'C2', '520.75', 4, 'operador2', [3]),
            ('AV202', 'Bogotá', 'Guayaquil', -4, 2, 'VUE', 'A2', '175.00', 0, 'jefe_vuelos', [0, 4]),
            ('LA2050', 'Santiago', 'Quito', -30, 5, 'ATE', 'B1', '410.00', 1, 'jefe_vuelos', [2]),
        ]
        for (cod, ori, des, h, dur, est, pue, pre, ae, cre, pas) in vuelos:
            salida = ahora + timedelta(hours=h)
            vuelo, _ = Vuelo.objects.update_or_create(
                codigo=cod, defaults={
                    'origen': ori, 'destino': des, 'fecha_salida': salida,
                    'fecha_llegada': salida + timedelta(hours=dur),
                    'estado': est, 'puerta': pue, 'precio_base': pre,
                    'avion': aviones[ae], 'creado_por': usuarios[cre]})
            vuelo.pasajeros.set([pasajeros[i] for i in pas])
       

    def _usuarios(self):
        usuarios = {}
        for username, clave, grupo in USUARIOS:
            user, _ = User.objects.get_or_create(
                username=username,
                defaults={'email': f'{username}@aeropuerto.test'})
            user.set_password(clave)
            if grupo is None:
                user.is_staff = user.is_superuser = True
            user.save()
            if grupo:
                user.groups.set([Group.objects.get(name=grupo)])
            usuarios[username] = user
        return usuarios
