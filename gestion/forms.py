from .models import Informacion
from django import forms
from .widget import DatePickerInput


class formularioInformacion(forms.ModelForm):

    fecha_modificacion = forms.DateField(widget=DatePickerInput)
    fecha_vencimiento = forms.DateField(widget=DatePickerInput)
    class Meta:
        model = Informacion
        fields = '__all__'
