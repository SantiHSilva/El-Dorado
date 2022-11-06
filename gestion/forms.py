from .models import Informacion
from django import forms

class formularioInformacion(forms.ModelForm):
    class Meta:
        model = Informacion
        fields = '__all__'
        widget = {'fecha_modificacion': forms.DateInput(attrs={'type': 'date', 'placeholder': 'XD'}), 'fecha_vencimiento': forms.DateInput(attrs={'type': 'date'})}