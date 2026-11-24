from django.contrib import admin
from .models import Aerolinea

@admin.register(Aerolinea)
class AerolineaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'codigo', 'pais')
    search_fields = ('nombre', 'codigo', 'pais')
    ordering = ('nombre',)
