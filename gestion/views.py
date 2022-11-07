from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest
from gestion.models import Informacion
from gestion.forms import formularioInformacion

# Create your views here.

class FormularioInformacionView(HttpRequest):
    def index(request):
        data = {
            'form': formularioInformacion()
        }
        if request.method == 'POST':
            formulario = formularioInformacion(data=request.POST, files=request.FILES)
            if formulario.is_valid():
                formulario.save()
                data["mensaje"] = "Guardado Correctamente"
            else:
                data["form"] = formulario
        return render(request, 'informacionIndex.html', data)

    def modificar_producto(request, id):
        producto = get_object_or_404(Informacion, id=id)
        print('producto:',producto.cantidad_productos)
        data = {
            'form': formularioInformacion(instance=producto)
        }
        print('data:',data['form'])
        if request.method == 'POST':
            formulario = formularioInformacion(data=request.POST, instance=producto, files = request.FILES)
            print("formulario:", formulario)
            if formulario.is_valid():
                producto.update(**formulario.cleaned_data)
                producto.save()
                return redirect(to='/')
            data["form"] = formulario
        return render(request, 'modificar_producto.html', data)
                
