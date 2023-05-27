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
from gestion.forms import *
from gestion.models import Informacion, Producto, Proveedores
from .utils import render_to_pdf, guardar_entrada, guardar_salida

# Create your views here.

# Formulario para el manejo de los productos

class FormularioInformacionView(HttpRequest):

    #Vista para la creación base de los productos

    @login_required
    def index(request):
        data = {
            'form': formularioInformacion()  # Se crea el formulario
        }
        if request.method == 'POST': # Si el método es POST
            formulario = formularioInformacion(data=request.POST) # Se crea el formulario con los datos del POST
            if formulario.is_valid(): # Si el formulario es válido
                formulario.save() # Se guarda el formulario
                messages.success(request, "Producto registrado correctamente") # Se muestra un mensaje de éxito
                return redirect(to='http://127.0.0.1:8000/lista/') # Se redirecciona a la lista de productos
            else:
                data["form"] = formulario # Si el formulario no es válido, se muestra el formulario con los errores
        return render(request, 'informacionIndex.html', data) # Se muestra el formulario

    #Vista para la creación de subproductos

    @login_required
    def agregar_producto(request):
        data ={
            'form': ProductoForm(),
        }
        if request.method == 'POST':
            formulario = ProductoForm(data=request.POST)
            # request first name and last name
            # print(request.user.first_name)
            # print(request.user.last_name)
            # print(request.POST)
            # print(acciones.ENTRADA.name)
            if formulario.is_valid():
                formulario.save()
                # autor = request.user.first_name + " " + request.user.last_name
                # guardar_entrada_salida(autor, request.POST["nombre_descripcion"], acciones.ENTRADA)
                messages.success(request, "Producto registrado correctamente")
                return redirect(to='http://127.0.0.1:8000/lista/')
            else:
                data["form"] = formulario
        return render(request, 'sub_productos.html', data)
    
    #Vista para la creación de proveedores

    @login_required
    def agregar_proveedor(request):
        data ={
            'form': formularioProveedores(),
        }
        if request.method == 'POST':
            formulario = formularioProveedores(data=request.POST)
            if formulario.is_valid():
                formulario.save()
                messages.success(request, "Proveedor registrado correctamente")
                return redirect(to='http://127.0.0.1:8000/proveedores/')
            else:
                data["form"] = formulario
        return render(request, 'proveedores.html', data)

    # Entrada de subproductos

    @login_required
    def entrada_producto(request, id):
        producto = get_object_or_404(Informacion, id=id)
        form = formularioEntradaInformacion(instance=producto)
        form.initial['cantidad_productos'] = 0
        data = {
            'form': form,
            'info': Informacion.objects.filter(id=id).get().producto,
            'actual' : Informacion.objects.filter(id=id).get().cantidad_productos
        }
        if request.method == 'POST':
            formulario = formularioEntradaInformacion(data=request.POST, instance=producto)
            print(f'Cantidad de productos: {formulario["cantidad_productos"].value()}')
            if formulario.is_valid():
                autor = request.user.first_name + " " + request.user.last_name
                producto = Informacion.objects.filter(id=id).get()
                guardar_entrada(
                    nombre = autor,
                    producto = Informacion.objects.filter(id=id).get().producto,
                    cantidad = formulario['cantidad_productos'].value(),
                    proveedor = formulario['proveedor'].value(),
                    )
                producto.cantidad_productos = int(producto.cantidad_productos) + int(formulario['cantidad_productos'].value())
                producto.save()
                messages.success(request, "Entrada registrada correctamente")
                return redirect(to='http://127.0.0.1:8000/lista/')
            else:
                data["form"] = formulario
        return render(request, 'entradas.html', data)
    
    # Salida de subproductos

    @login_required
    def salida_informacion(request, id):
        producto = get_object_or_404(Informacion, id=id)
        form = formularioSalidaInformacion(instance=producto)
        form.initial['cantidad_productos'] = 0
        data = {
            'form': form,
            'info': Informacion.objects.filter(id=id).get().producto,
            'actual' : Informacion.objects.filter(id=id).get().cantidad_productos
        }
        if request.method == 'POST':
            formulario = formularioSalidaInformacion(data=request.POST, instance=producto)
            if formulario.is_valid():
                producto = Informacion.objects.filter(id=id).get()
                autor = request.user.first_name + " " + request.user.last_name
                guardar_salida(
                    nombre = autor,
                    producto = Informacion.objects.filter(id=id).get().producto,
                    cantidad = formulario['cantidad_productos'].value(),
                    proveedor = formulario['proveedor'].value(),
                    razon = formulario['razon_salida'].value(),
                    )
                producto.cantidad_productos = int(producto.cantidad_productos) - int(formulario['cantidad_productos'].value())
                producto.save()
                messages.success(request, "Salida registrada correctamente")
                return redirect(to='http://127.0.0.1:8000/lista/')
            else:
                data["form"] = formulario
        return render(request, 'salidas.html', data)
    #Vista para la edición del subproducto

    @login_required
    def modificar_producto(request, id):
        producto = get_object_or_404(Informacion, id=id)
        data = {
            'form': formularioInformacion(instance=producto),
            'info': Informacion.objects.filter(id=id).get().producto
        }
        if request.method == 'POST':
            formulario = formularioInformacion(data=request.POST, instance=producto)
            if formulario.is_valid():
                producto.save()
                messages.success(request, "Subproducto modificado correctamente")
                return redirect(to='http://127.0.0.1:8000/lista/')
            data["form"] = formulario
        return render(request, 'modificar_producto.html', data)
    
    #Vista para la edición del proveedor

    @login_required
    def modificar_proveedor(request, id):
        proveedor = get_object_or_404(Proveedores, id=id)
        data = {
            'form': formularioProveedores(instance=proveedor),
            'info': Proveedores.objects.filter(id=id).get()
        }
        if request.method == 'POST':
            formulario = formularioProveedores(data=request.POST, instance=proveedor)
            if formulario.is_valid():
                proveedor.save()
                messages.success(request, "Proveedor modificado correctamente")
                return redirect(to='http://127.0.0.1:8000/proveedores/')
            data["form"] = formulario
        return render(request, 'modificar_proveedor.html', data)

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
    
    #Vista para la eliminación del proveedor

    @login_required
    def eliminar_proveedor(request, id):
        proveedor = get_object_or_404(Proveedores, id=id)
        proveedor.delete()
        messages.success(request, "Proveedor eliminado correctamente")
        return redirect(to='http://127.0.0.1:8000/proveedores/')
#Exportación de resultados globales a pdf

class exportResultadosPDF(View):
    def get(self, request, *args, **kwargs):
        #Declaración de variables
        info, productos, cantidad, cantidades, total_informacion_por_producto ,fecha_vencimiento, cantidad_peso, vencidos, por_caducar= [], [], [], [], [], [], [], [], []
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
            fecha_vencimiento = time.mktime(objeto['fecha_vencimiento'].timetuple())  # Fecha de vencimiento
            ahora = time.mktime(datetime.now().timetuple()) # Fecha actual
            for producto in Producto.objects.values(): # Se recorre la lista de productos
                if producto["id_producto"] == objeto["producto_id"]: # Si el id del producto es igual al id del producto de la información
                    if fecha_vencimiento < ahora: # Si la fecha de vencimiento es menor a la fecha actual
                        # Se agrega el producto a la lista de vencidos
                        vencidos.append(f"({producto['id_producto']}) Producto: {producto['nombre_descripcion']}, P-ID: {objeto['id']}: vencio hace: {(abs(datetime.strptime(str(objeto['fecha_vencimiento']), fmt) - datetime.now()).days)+1} días")
                    if (fecha_vencimiento - ahora) <= 864000: # Si la fecha de vencimiento es menor a 10 días
                        # Se agrega el producto a la lista de por caducar
                        if ahora < fecha_vencimiento:
                            por_caducar.append(f"({producto['id_producto']}) Producto: {producto['nombre_descripcion']}, P-ID: {objeto['id']}: vencera en: {((datetime.strptime(str(objeto['fecha_vencimiento']), fmt) - datetime.now()).days)+1} días")
        
        #Sumatoria de las cantidades de los productos por cantidad
        for cantidad_producto in cantidad: # Se recorre la lista de cantidades de productos
            for producto in productos: # Se recorre la lista de productos 
                if cantidad_producto[0] == producto.id_producto: # Si el id del producto es igual al id del producto de la información
                    setattr(producto, 'cantidad', (producto.cantidad + cantidad_producto[1])) # Se le suma la cantidad de productos a la cantidad de productos del producto

        #Sumatoria de las cantidades de los productos por peso
        for cantidad_producto in cantidad_peso: # Se recorre la lista de cantidades de productos
            for producto in productos: # Se recorre la lista de productos
                if cantidad_producto[0] == producto.id_producto: # Si el id del producto es igual al id del producto de la información
                    setattr(producto, 'cantidad_peso', (producto.cantidad_peso + cantidad_producto[1])) # Se le suma la cantidad de productos a la cantidad de productos del producto
        #Diagrama de barras de la cantidade de información por producto base
        #Obtención de datos para el diagrama de barras de la cantidad de información por producto base
        total_nombre_productos = (list(Producto.objects.values_list('nombre_descripcion', flat=True))) # Se obtiene una lista con los nombres de los productos
        for i in (Producto.objects.values_list('id_producto', flat=True)): # Se recorre la lista de id de productos
            total_informacion_por_producto.append(Informacion.objects.filter(producto_id=i).count()) # Se obtiene la cantidad de información por producto y se agrega a la lista de total de información por producto

        
        #Configuración de la gráfica
        fig2, ax2 = plt.subplots() # Se crea la figura y los ejes
        ax2.barh(total_nombre_productos, total_informacion_por_producto, align='center', height=0.3) # Se crea la gráfica de barras
        fig2.tight_layout() # Se ajusta la gráfica
        fig2.savefig("static/grafico2.png") # Se guarda la gráfica en la carpeta static

        #Creación de la tabla de resultados globales
        #Definición de variables
        all_count = Producto.objects.filter(categoria_producto="1").count() #Conteo de productos tipo Alimento
        all_count2 = Producto.objects.filter(categoria_producto="2").count() #Conteo de productos tipo Bebida
        all_count3 = Producto.objects.filter(categoria_producto="3").count() #Conteo de productos tipo Limpieza
        all_count4 = Producto.objects.filter(categoria_producto="4").count() #Conteo de productos tipo Otros

        #Configuración de la tabla
        labels = 'Alimentos', 'Bebidas', 'Limpieza', 'Otros'
        sizes = [all_count, all_count2, all_count3, all_count4]
        fig, ax = plt.subplots()
        ax.pie(sizes, autopct=make_autopct(sizes))
        ax.legend(labels, loc='upper right')
        ax.set_aspect('equal')

        #Guardar tabla
        fig.savefig("static/grafico.png" , bbox_inches='tight', pad_inches=0.0) 

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
            'all_cat1' : Producto.objects.filter(categoria_producto="1").values, # Información de los productos de la categoria de Alimentos
            'cont_cat1' : all_count,
            #Información de los productos de la categoria de Bebidas
            'all_cat2' : Producto.objects.filter(categoria_producto="2").values, # Información de los productos de la categoria de Bebidas
            'cont_cat2' : all_count2,
            #Información de los productos de la categoria de Limpieza 
            'all_cat3' : Producto.objects.filter(categoria_producto="3").values, # Información de los productos de la categoria de Limpieza
            'cont_cat3' : all_count3,
            #Información de los productos de la categoria de Otros
            'all_cat4' : Producto.objects.filter(categoria_producto="4").values, # Información de los productos de la categoria de Otros
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