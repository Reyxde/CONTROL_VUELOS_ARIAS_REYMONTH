from django.contrib import admin
from .models import Aerolinea, Avion

@admin.register(Aerolinea)
class AerolineaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'codigo', 'pais')
    search_fields = ('nombre', 'codigo', 'pais')
    ordering = ('nombre',)


@admin.register(Avion)
class AvionAdmin(admin.ModelAdmin):
    list_display = ('matricula', 'modelo', 'capacidad', 'estado', 'aerolinea')
    list_filter = ('estado', 'aerolinea')
    search_fields = ('matricula', 'modelo', 'aerolinea__nombre')
    ordering = ('matricula',)
