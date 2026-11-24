from django.db import models
from django.urls import reverse

from .aerolinea import Aerolinea


class Avion(models.Model):
    class Estado(models.TextChoices):
        OPERATIVA = 'OPE', 'Operativa'
        MANTENIMIENTO = 'MAN', 'En mantenimiento'
        FUERA_SERVICIO = 'FUE', 'Fuera de servicio'

    matricula = models.CharField('matrícula', max_length=10, unique=True)
    modelo = models.CharField(max_length=100)
    capacidad = models.PositiveIntegerField('capacidad de pasajeros')
    fecha_fabricacion = models.DateField('fecha de fabricación')
    estado = models.CharField(
        max_length=3, choices=Estado.choices, default=Estado.OPERATIVA)
    aerolinea = models.ForeignKey(
        Aerolinea, on_delete=models.PROTECT, related_name='aviones',
        verbose_name='aerolínea')

    class Meta:
        verbose_name = 'avión'
        verbose_name_plural = 'aviones'
        ordering = ['matricula']

    def __str__(self):
        return f'{self.matricula} - {self.modelo}'

    def get_absolute_url(self):
        return reverse('avion_detail', args=[self.pk])
