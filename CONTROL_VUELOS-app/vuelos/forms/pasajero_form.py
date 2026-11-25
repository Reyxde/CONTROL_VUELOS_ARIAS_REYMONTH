from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from vuelos.models import Pasajero


class PasajeroForm(forms.ModelForm):
    class Meta:
        model = Pasajero
        fields = ['nombre', 'apellido', 'documento', 'nacionalidad',
                  'fecha_nacimiento']
        widgets = {
            'fecha_nacimiento': forms.DateInput(
                format='%Y-%m-%d', attrs={'type': 'date'}),
        }

    def clean_fecha_nacimiento(self):
        fecha = self.cleaned_data['fecha_nacimiento']
        if fecha > timezone.localdate():
            raise ValidationError('La fecha de nacimiento no puede ser futura.')
        return fecha
