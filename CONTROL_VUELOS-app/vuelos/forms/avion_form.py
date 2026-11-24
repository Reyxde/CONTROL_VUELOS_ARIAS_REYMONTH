from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from vuelos.models import Avion


class AvionForm(forms.ModelForm):
    class Meta:
        model = Avion
        fields = [
            'matricula', 'modelo', 'capacidad', 'fecha_fabricacion',
            'estado', 'aerolinea',
        ]
        widgets = {
            'fecha_fabricacion': forms.DateInput(
                format='%Y-%m-%d', attrs={'type': 'date'}),
        }

    def clean_matricula(self):
        return self.cleaned_data['matricula'].strip().upper()

    def clean_capacidad(self):
        capacidad = self.cleaned_data['capacidad']
        if capacidad < 1:
            raise ValidationError('La capacidad debe ser mayor que cero.')
        return capacidad

    def clean_fecha_fabricacion(self):
        fecha = self.cleaned_data['fecha_fabricacion']
        if fecha > timezone.localdate():
            raise ValidationError('La fecha de fabricación no puede ser futura.')
        return fecha
