from django.contrib import admin

from .models import Aerolinea, Avion, Pasajero, Vuelo


@admin.register(Aerolinea)
class AerolineaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'codigo', 'pais')
    list_filter = ('pais',)
    search_fields = ('nombre', 'codigo', 'pais')
    ordering = ('nombre',)


@admin.register(Avion)
class AvionAdmin(admin.ModelAdmin):
    list_display = ('matricula', 'modelo', 'capacidad', 'estado', 'aerolinea')
    list_filter = ('estado', 'aerolinea')
    search_fields = ('matricula', 'modelo', 'aerolinea__nombre')
    ordering = ('matricula',)


@admin.register(Pasajero)
class PasajeroAdmin(admin.ModelAdmin):
    list_display = ('apellido', 'nombre', 'documento', 'nacionalidad',
                    'fecha_nacimiento')
    list_filter = ('nacionalidad',)
    search_fields = ('nombre', 'apellido', 'documento')
    ordering = ('apellido', 'nombre')


@admin.register(Vuelo)
class VueloAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'origen', 'destino', 'fecha_salida', 'estado',
                    'avion', 'creado_por')
    list_filter = ('estado', 'avion__aerolinea', 'fecha_salida')
    search_fields = ('codigo', 'origen', 'destino')
    filter_horizontal = ('pasajeros',)
    ordering = ('fecha_salida',)