from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest
from gestion.models import Informacion
from gestion.forms import formularioInformacion

# Create your views here.

class FormularioInformacionView(HttpRequest):
    def index(request):
        info = formularioInformacion()
        return render(request, 'informacionIndex.html', {'form': info})

    def procesar_formulario(request):
        return render(request, 'informacionIndex.html', {'form': info, 'mensaje': 'OK'})

    def modificar_producto(request, id):
        producto = get_object_or_404(Informacion, id=id)
        data = {
            'form': formularioInformacion(instance=producto)
        }
        return render(request, 'modificar_producto.html', data)
