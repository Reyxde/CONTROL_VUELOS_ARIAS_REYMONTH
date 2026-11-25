from django import forms
from django.core.exceptions import ValidationError

from vuelos.models import Avion, Vuelo

FORMATO_FECHA_HORA = '%Y-%m-%dT%H:%M'


class VueloForm(forms.ModelForm):
    class Meta:
        model = Vuelo
        fields = ['codigo', 'origen', 'destino', 'aeronave', 'fecha_salida',
                  'fecha_llegada', 'estado', 'puerta', 'precio_base',
                  'pasajeros']
        widgets = {
            'fecha_salida': forms.DateTimeInput(
                format=FORMATO_FECHA_HORA, attrs={'type': 'datetime-local'}),
            'fecha_llegada': forms.DateTimeInput(
                format=FORMATO_FECHA_HORA, attrs={'type': 'datetime-local'}),
            'pasajeros': forms.CheckboxSelectMultiple,
        }

    def clean_codigo(self):
        return self.cleaned_data['codigo'].strip().upper()

    def clean_precio_base(self):
        precio = self.cleaned_data['precio_base']
        if precio <= 0:
            raise ValidationError('El precio debe ser mayor que cero.')
        return precio

    def clean(self):
        datos = super().clean()
        origen = datos.get('origen')
        destino = datos.get('destino')
        salida = datos.get('fecha_salida')
        llegada = datos.get('fecha_llegada')
        aeronave = datos.get('aeronave')
        pasajeros = datos.get('pasajeros')

        if origen and destino and origen.strip().lower() == destino.strip().lower():
            raise ValidationError('El origen y el destino no pueden ser iguales.')
        if salida and llegada and llegada <= salida:
            raise ValidationError('La llegada debe ser posterior a la salida.')
        if aeronave and (self.instance.pk is None
                         or 'aeronave' in self.changed_data):
            if aeronave.estado != Avion.Estado.OPERATIVA:
                self.add_error(
                    'aeronave', 'Solo se pueden asignar aeronaves operativas.')
        if aeronave and pasajeros is not None and len(pasajeros) > aeronave.capacidad:
            self.add_error(
                'pasajeros',
                f'La aeronave solo admite {aeronave.capacidad} pasajeros.')
        return datos
