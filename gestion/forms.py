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

class formularioEntradaInformacion(forms.ModelForm):
    # Solo poder modificar la cantidad de productos
    class Meta:
        model = Informacion
        fields = ['cantidad_productos']
    cantidad_productos = forms.IntegerField(required=True, min_value=1, label="", help_text="Ingrese la cantidad de productos a adicionar")  

class formularioSalidaInformacion(forms.ModelForm):
    # Solo poder modificar la cantidad de productos
    class Meta:
        model = Informacion
        fields = ['cantidad_productos']
    cantidad_productos = forms.IntegerField(required=True, min_value=1, label="", help_text="Ingrese la cantidad de productos a retirar") 
    razon_salida_opciones = (('1', 'Consumo'), ('2', 'Dañado'), ('3', 'Donación'), ('4', 'Otros'))
    razon_salida = forms.ChoiceField(choices=razon_salida_opciones, label="", help_text="Seleccione la razón de la salida") 

#Formulario para la edición o adición de proveedores

class formularioProveedores(forms.ModelForm):
    class Meta:
        model = Proveedores
        fields = '__all__'
