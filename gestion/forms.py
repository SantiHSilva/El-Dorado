from .models import Informacion, Producto, Proveedores
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
    proveedor = forms.ModelChoiceField(queryset=Proveedores.objects.all())
    class Meta:
        model = Informacion
        fields = '__all__'

#Formulario para la edición o adición de proveedores

class formularioProveedores(forms.ModelForm):
    class Meta:
        model = Proveedores
        fields = '__all__'
