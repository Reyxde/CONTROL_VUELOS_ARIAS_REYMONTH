from django.db import models
from django.urls import reverse


class Pasajero(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    documento = models.CharField('documento de identidad', max_length=20,
                                 unique=True)
    nacionalidad = models.CharField(max_length=100, blank=True)
    fecha_nacimiento = models.DateField('fecha de nacimiento')

    class Meta:
        verbose_name = 'pasajero'
        verbose_name_plural = 'pasajeros'
        ordering = ['apellido', 'nombre']

    def __str__(self):
        return f'{self.apellido}, {self.nombre}'

    def get_absolute_url(self):
        return reverse('pasajero_detail', args=[self.pk])
