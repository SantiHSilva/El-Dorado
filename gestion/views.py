from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse
from gestion.models import Informacion
from gestion.forms import formularioInformacion
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import date
from django.views.generic import View
from .utils import render_to_pdf

# Create your views here.

class exportResultadosPDF(View):
    def get(self, request, *args, **kwargs):
        data = {
            'informacion': Informacion.objects.all(),
            'date' : date.today(),
        }
        pdf = render_to_pdf('exportTabla.html', data)
        return HttpResponse(pdf, content_type='application/pdf')

class FormularioInformacionView(HttpRequest):
    @login_required
    def index(request):
        data = {
            'form': formularioInformacion()
        }
        if request.method == 'POST':
            formulario = formularioInformacion(data=request.POST, files=request.FILES)
            if formulario.is_valid():
                print(formulario)
                formulario.save()
                messages.success(request, "Producto registrado correctamente")
                return redirect(to='http://127.0.0.1:8000/lista/')
            else:
                data["form"] = formulario
        return render(request, 'informacionIndex.html', data)

    @login_required
    def modificar_producto(request, id):
        producto = get_object_or_404(Informacion, id=id)
        # print('producto:',producto.cantidad_productos)
        data = {
            'form': formularioInformacion(instance=producto),
            'info': Informacion.objects.get(id=id)
        }
        if request.method == 'POST':
            formulario = formularioInformacion(data=request.POST, instance=producto, files = request.FILES)
            if formulario.is_valid():
                producto.save()
                messages.success(request, "Producto modificado correctamente")
                return redirect(to='http://127.0.0.1:8000/lista/')
            data["form"] = formulario
        return render(request, 'modificar_producto.html', data)
    
    @login_required
    def eliminar_producto(request, id):
        producto = get_object_or_404(Informacion, id=id)
        producto.delete()
        messages.success(request, "Producto eliminado correctamente")
        return redirect(to='http://127.0.0.1:8000/lista/')
