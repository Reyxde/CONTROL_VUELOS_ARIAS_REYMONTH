from django import forms

from vuelos.models import Aerolinea


class AerolineaForm(forms.ModelForm):
    class Meta:
        model = Aerolinea
        fields = ['nombre', 'codigo', 'pais']

    def clean_codigo(self):
        return self.cleaned_data['codigo'].strip().upper()
