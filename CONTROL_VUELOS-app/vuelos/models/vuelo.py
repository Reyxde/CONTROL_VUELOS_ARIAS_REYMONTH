from django.conf import settings
from django.db import models
from django.urls import reverse

from .avion import Avion
from .pasajero import Pasajero


class Vuelo(models.Model):
    class Estado(models.TextChoices):
        PROGRAMADO = 'PRO', 'Programado'
        EMBARCANDO = 'EMB', 'Embarcando'
        EN_VUELO = 'VUE', 'En vuelo'
        ATERRIZADO = 'ATE', 'Aterrizado'
        RETRASADO = 'RET', 'Retrasado'
        CANCELADO = 'CAN', 'Cancelado'

    codigo = models.CharField('código de vuelo', max_length=10, unique=True)
    origen = models.CharField(max_length=100)
    destino = models.CharField(max_length=100)
    fecha_salida = models.DateTimeField('salida')
    fecha_llegada = models.DateTimeField('llegada')
    estado = models.CharField(
        max_length=3, choices=Estado.choices, default=Estado.PROGRAMADO)
    puerta = models.CharField('puerta de embarque', max_length=5, blank=True)
    
    precio_base = models.DecimalField(
        'precio base (USD)', max_digits=8, decimal_places=2)
    
    aeronave = models.ForeignKey(
        Avion, on_delete=models.PROTECT, related_name='vuelos')
    pasajeros = models.ManyToManyField(
        Pasajero, related_name='vuelos', blank=True)
    
    creado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='vuelos_creados',
        verbose_name='creado por')

    class Meta:
        verbose_name = 'vuelo'
        verbose_name_plural = 'vuelos'
        ordering = ['fecha_salida']

    def __str__(self):
        return f'{self.codigo}: {self.origen} → {self.destino}'

    def get_absolute_url(self):
        return reverse('vuelo_detail', args=[self.pk])
