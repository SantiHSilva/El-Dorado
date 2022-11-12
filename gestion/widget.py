from django import forms

#Clase para el formulario tipo fecha

class DatePickerInput(forms.DateInput):
    input_type = 'date'