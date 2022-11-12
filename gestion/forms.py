from .models import Informacion, Producto
from django import forms
from .widget import DatePickerInput

#Formulario para la edición o adición de productos base

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'

#Formulario para la edición o adición de subproductos

class formularioInformacion(forms.ModelForm):
    fecha_modificacion = forms.DateField(widget=DatePickerInput)
    fecha_vencimiento = forms.DateField(widget=DatePickerInput)
    class Meta:
        model = Informacion
        fields = '__all__'
