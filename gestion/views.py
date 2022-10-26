from django.shortcuts import render
from django.http import HttpRequest

from gestion.forms import formularioInformacion

# Create your views here.

class FormularioInformacionView(HttpRequest):
    def index(request):
        info = formularioInformacion()
        return render(request, 'informacionIndex.html', {'form': info})

    def procesar_formulario(request):
        info = formularioInformacion(request.POST)
        if info.is_valid():
            info.save()
            info = formularioInformacion()
        return render(request, 'informacionIndex.html', {'form': info, 'mensaje': 'OK'})
