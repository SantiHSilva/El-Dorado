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

# Formulario para el manejo de los productos

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
            'info': Producto
        }
        if request.method == 'POST':
            formulario = formularioInformacion(data=request.POST, instance=producto, files = request.FILES)
            if formulario.is_valid():
                producto.save()
                messages.success(request, "Subproducto modificado correctamente")
                return redirect(to='http://127.0.0.1:8000/lista/')
            data["form"] = formulario
        return render(request, 'modificar_producto.html', data)

    #Vista para la edición del producto base

    @login_required
    def modificar_base(request, id):
        producto = get_object_or_404(Producto, id_producto=id)
        data = {
            'producto' : Producto.objects.filter(id_producto=id).get(),
            'form': ProductoForm(instance=producto),
        }
        if request.method == 'POST':
            formulario = ProductoForm(data=request.POST, instance=producto, files = request.FILES)
            if formulario.is_valid():
                producto.save()
                messages.success(request, "Producto base modificado correctamente")
                return redirect(to='http://127.0.0.1:8000/lista/')
            data["form"] = formulario
        return render(request, 'modificar_producto.html', data)
    
    #Vista para la eliminación del producto base

    @login_required
    def eliminar_productoBase(request, id):
        producto = get_object_or_404(Producto, id_producto=id)
        producto.delete()
        messages.success(request, "Producto base eliminado correctamente")
        return redirect(to='http://127.0.0.1:8000/lista/')

    #Vista para la eliminación del subproductos

    @login_required
    def eliminar_subProductos(request, id):
        producto = get_object_or_404(Informacion, id=id)
        producto.delete()
        messages.success(request, "Subproducto eliminado correctamente")
        return redirect(to='http://127.0.0.1:8000/lista/')


#Exportación de resultados globales a pdf

class exportResultadosPDF(View):
    def get(self, request, *args, **kwargs):
        #Declaración de variables
        info, productos, cantidad, cantidades, fecha_vencimiento, cantidad_peso, vencidos, por_caducar= [], [], [], [], [], [], [], []
        suma_cantidad = 0
        BASE_DIR = Path(__file__).resolve().parent.parent
        fmt = "%Y-%m-%d"
        
        #Creación de atributos para la sumatoria de los productos por información
        for conjunto_producto in Producto.objects.all():
            setattr(conjunto_producto, 'cantidad', 0)
            setattr(conjunto_producto, 'cantidad_peso', 0)
            productos.append(conjunto_producto)

        #Creación de atributos para la sumatoria todos los productos y filtrar los productos por vencimiento
        for objeto in Informacion.objects.values():
            #Stock reserva
            objeto["stock_reserva"] = int(objeto["cantidad_productos"]*0.2) 
            info.append(objeto)
            #Sumatoria de las cantidades de la información de los productos
            cantidades.append(objeto['cantidad_productos'])
            suma_cantidad = int((sp.integrate(1, (x,0,objeto["cantidad_productos"])))) + int(suma_cantidad)
            #Sumatoria de las cantidades de la información de los productos por peso
            cantidad.append([objeto['producto_id'],objeto["cantidad_productos"]])
            cantidad_peso.append([objeto['producto_id'],objeto["peso_unidad"]])
            #Filtrado de productos por vencimiento
            fecha_vencimiento = time.mktime(objeto['fecha_vencimiento'].timetuple()) 
            ahora = time.mktime(datetime.now().timetuple())
            for producto in Producto.objects.values():
                if producto["id_producto"] == objeto["producto_id"]:
                    if fecha_vencimiento < ahora:
                        vencidos.append(f"({producto['id_producto']}) Producto: {producto['nombre_descripcion']}, P-ID: {objeto['id']}: vencio hace: {(abs(datetime.strptime(str(objeto['fecha_vencimiento']), fmt) - datetime.now()).days)+1} días")
                    if (fecha_vencimiento - ahora) <= 864000:
                        if ahora < fecha_vencimiento:
                            por_caducar.append(f"({producto['id_producto']}) Producto: {producto['nombre_descripcion']}, P-ID: {objeto['id']}: vencera en: {((datetime.strptime(str(objeto['fecha_vencimiento']), fmt) - datetime.now()).days)+1} días")
        
        #Sumatoria de las cantidades de los productos por cantidad
        for cantidad_producto in cantidad:
            for producto in productos:
                if cantidad_producto[0] == producto.id_producto:
                    setattr(producto, 'cantidad', (producto.cantidad + cantidad_producto[1]))

        #Sumatoria de las cantidades de los productos por peso
        for cantidad_producto in cantidad_peso:
            for producto in productos:
                if cantidad_producto[0] == producto.id_producto:
                    setattr(producto, 'cantidad_peso', (producto.cantidad_peso + cantidad_producto[1]))

        #Creación de la tabla de resultados globales
        #Definición de variables
        all_count = Producto.objects.filter(categoria_producto="1").count()
        all_count2 = Producto.objects.filter(categoria_producto="2").count()
        all_count3 = Producto.objects.filter(categoria_producto="3").count()
        all_count4 = Producto.objects.filter(categoria_producto="4").count()
        #Configuración de la tabla
        labels = 'Alimentos', 'Bebidas', 'Limpieza', 'Otros'
        sizes = [all_count, all_count2, all_count3, all_count4]
        fig, ax = plt.subplots()
        ax.pie(sizes, autopct=make_autopct(sizes))
        ax.legend(labels, loc='upper right')
        ax.set_aspect('equal')
        #Guardar tabla
        plt.savefig("static/grafico.png" , bbox_inches='tight', pad_inches=0.0) 

        #Datos globales para la utlización de la plantilla
        data = {
            #Información de los productos
            'info' : info,
            #Path para ingresar imagenes de Static
            'path' : path.join(BASE_DIR, 'static'),     
            #Fecha de generación
            'date' : date.today(),                  
            #Hora de generación    
            'time' : time.strftime("%H:%M:%S"),      
            #Información de los productos base
            'producto' : productos,
            'productos' : Producto.objects.values(),
            #Sumatoria de las cantidades de los productos por separado
            'suma_cantidad' : suma_cantidad,
            #Hallar el producto con mayor cantidad
            'max_number' : max(cantidades),
            #Información del producto con mayor cantidad
            'max_number_info' : Informacion.objects.filter(cantidad_productos=max(cantidades)).values,
            #Hallar el producto con menor cantidad
            'min_number' : min(cantidades),
            #Información del producto con menor cantidad
            'min_number_info' : Informacion.objects.filter(cantidad_productos=min(cantidades)).values,
            #Información de los productos de la categoria de Alimentos
            'all_cat1' : Producto.objects.filter(categoria_producto="1").values,
            'cont_cat1' : all_count,
            #Información de los productos de la categoria de Bebidas
            'all_cat2' : Producto.objects.filter(categoria_producto="2").values,
            'cont_cat2' : all_count2,
            #Información de los productos de la categoria de Limpieza
            'all_cat3' : Producto.objects.filter(categoria_producto="3").values,
            'cont_cat3' : all_count3,
            #Información de los productos de la categoria de Otros
            'all_cat4' : Producto.objects.filter(categoria_producto="4").values,
            'cont_cat4' : all_count4,
            #Información de los productos vencidos
            'vencidos' : vencidos,
            #Información de los productos por caducar
            'por_caducar': por_caducar,
        }
        #Renderizado de la plantilla
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