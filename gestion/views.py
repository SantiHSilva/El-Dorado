import time
from datetime import date, datetime
from os import path
from pathlib import Path

import matplotlib.pyplot as plt
import sympy as sp
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import View
from sympy.abc import x

from gestion.forms import formularioInformacion, ProductoForm
from gestion.models import Informacion, Producto

from .utils import render_to_pdf


# Create your views here.

#Formulario para el manejo de los productos

class FormularioInformacionView(HttpRequest):

    #Vista para la creación base de los productos

    @login_required
    def index(request):
        data = {
            'form': formularioInformacion()
        }
        if request.method == 'POST':
            formulario = formularioInformacion(data=request.POST, files=request.FILES)
            if formulario.is_valid():
                formulario.save()
                messages.success(request, "Producto registrado correctamente")
                return redirect(to='http://127.0.0.1:8000/lista/')
            else:
                data["form"] = formulario
        return render(request, 'informacionIndex.html', data)

    #Vista para la creación de subproductos

    @login_required
    def agregar_producto(request):
        data ={
            'form': ProductoForm(),
        }
        if request.method == 'POST':
            formulario = ProductoForm(data=request.POST)
            if formulario.is_valid():
                formulario.save()
                messages.success(request, "Producto registrado correctamente")
                return redirect(to='http://127.0.0.1:8000/lista/')
            else:
                data["form"] = formulario
        return render(request, 'sub_productos.html', data)

    #Vista para la edición del subproducto

    @login_required
    def modificar_producto(request, id):
        producto = get_object_or_404(Informacion, id=id)
        data = {
            'form': formularioInformacion(instance=producto),
            'info': Producto.objects.get(id_producto=id)
        }
        if request.method == 'POST':
            formulario = formularioInformacion(data=request.POST, instance=producto, files = request.FILES)
            if formulario.is_valid():
                producto.save()
                messages.success(request, "Producto modificado correctamente")
                return redirect(to='http://127.0.0.1:8000/lista/')
            data["form"] = formulario
        return render(request, 'modificar_producto.html', data)

    #Vista para la edición del producto base

    @login_required
    def modificar_base(request, id):
        producto = get_object_or_404(Producto, id_producto=id)
        data = {
            'form': ProductoForm(instance=producto),
        }
        if request.method == 'POST':
            formulario = ProductoForm(data=request.POST, instance=producto, files = request.FILES)
            if formulario.is_valid():
                producto.save()
                messages.success(request, "Producto modificado correctamente")
                return redirect(to='http://127.0.0.1:8000/lista/')
            data["form"] = formulario
        return render(request, 'modificar_producto.html', data)
    
    #Vista para la eliminación del producto base

    @login_required
    def eliminar_producto(request, id):
        producto = get_object_or_404(Informacion, id=id)
        producto.delete()
        messages.success(request, "Producto eliminado correctamente")
        return redirect(to='http://127.0.0.1:8000/lista/')


#Exportación de resultados globales a pdf

class exportResultadosPDF(View):
    def get(self, request, *args, **kwargs):
        BASE_DIR = Path(__file__).resolve().parent.parent
        date_now = datetime.now()
        suma_peso, suma_cantidad = 0, 0
        productos, cantidades, por_caducar, vencidos = [], [], [], []
        fmt = "%Y-%m-%d"
        for objeto in Informacion.objects.values():
            suma_cantidad = int((sp.integrate(1, (x,0,objeto["cantidad_productos"])))) + int(suma_cantidad)
            if objeto["unidades"] == "2":
                suma_peso = g_a_kg((sp.integrate(1, (x,0,objeto["peso_unidad"])))) + suma_peso
            else:
                suma_peso = float((sp.integrate(1, (x,0,objeto["peso_unidad"])))) + suma_peso
            auxiliar = []
            auxiliar.append(objeto['nombre_descripcion'])
            auxiliar.append(objeto['cantidad_productos'])
            cantidades.append(objeto['cantidad_productos'])
            productos.append(auxiliar)
            fecha_vencimiento = time.mktime(objeto['fecha_vencimiento'].timetuple()) 
            ahora = time.mktime(date_now.timetuple())
            if fecha_vencimiento < ahora:
                vencidos.append(f"ID: {objeto['id']}: {objeto['nombre_descripcion']}, vencio hace: {abs(datetime.strptime(str(objeto['fecha_vencimiento']), fmt) - date_now).days} días")
            if (fecha_vencimiento - ahora) <= 864000:
                if ahora < fecha_vencimiento:
                    por_caducar.append(f"ID: {objeto['id']}: {objeto['nombre_descripcion']}, vencera en: {(datetime.strptime(str(objeto['fecha_vencimiento']), fmt) - date_now).days} días")
        all_count = Informacion.objects.filter(categoria_producto="1").count()
        all_count2 = Informacion.objects.filter(categoria_producto="2").count()
        all_count3 = Informacion.objects.filter(categoria_producto="3").count()
        all_count4 = Informacion.objects.filter(categoria_producto="4").count()
        labels = 'Alimentos', 'Bebidas', 'Limpieza', 'Otros'
        sizes = [all_count, all_count2, all_count3, all_count4]
        fig, ax = plt.subplots()
        ax.pie(sizes, autopct=make_autopct(sizes))
        ax.legend(labels, loc='upper right')
        ax.set_aspect('equal')
        plt.savefig("static/grafico.png" , bbox_inches='tight', pad_inches=0.0)
        data = {
            'informacion': Informacion.objects.all(),
            'date' : date.today(),
            'path' : path.join(BASE_DIR, 'static'),
            'time' : time.strftime("%H:%M:%S"),
            'max' : max(cantidades),
            'maxinfo' : Informacion.objects.filter(cantidad_productos=max(cantidades)),
            'min' : min(cantidades),
            'mininfo' : Informacion.objects.filter(cantidad_productos=min(cantidades)),
            'total' : Informacion.objects.count(),
            'all_cat1' : Informacion.objects.filter(categoria_producto="1").values,
            'cont_cat1' : all_count,
            'all_cat2' : Informacion.objects.filter(categoria_producto="2").values,
            'cont_cat2' : all_count2,
            'all_cat3' : Informacion.objects.filter(categoria_producto="3").values,
            'cont_cat3' : all_count3,
            'all_cat4' : Informacion.objects.filter(categoria_producto="4").values,
            'cont_cat4' : all_count4,
            'vencidos' : vencidos,
            'por_caducar': por_caducar,
            'suma_cantidad' : suma_cantidad,
        }
        pdf = render_to_pdf('exportTabla.html', data)
        return HttpResponse(pdf, content_type='application/pdf')

#Funciónes utilizadas

def make_autopct(values):
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        return '{p:.2f}%\n({v:d})'.format(p=pct,v=val)
    return my_autopct

def g_a_kg(valor):
    return valor / 1000