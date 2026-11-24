from django.db import models
from django.urls import reverse


class Aerolinea(models.Model):
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=3, unique=True)
    pais = models.CharField('país', max_length=100)

    class Meta:
        verbose_name = 'aerolínea'
        verbose_name_plural = 'aerolíneas'
        ordering = ['nombre']

    def __str__(self):
        return f'{self.nombre} ({self.codigo})'

    def get_absolute_url(self):
        return reverse('aerolinea_detail', args=[self.pk])
