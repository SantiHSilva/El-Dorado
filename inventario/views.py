from django.shortcuts import render
import numpy as np
import sympy as sp
from sympy.abc import x
import numpy.linalg as lin
from gestion.models import Informacion, Producto, Proveedores
from django.contrib.auth.decorators import login_required

#Vista base

def inicial(request):
    return render(request, "base.html")

#Vista de la auditoria

@login_required
def auditoria(request):
    return render(request, "entradas_salidas.html")

#Vista de la tabla general de los productos

@login_required
def lista_completa(request):
    #Definir las variables
    info, productos, cantidad = [], [], []
    suma_cantidad = 0

    #Obtener la cantidad de productos
    for objeto in Informacion.objects.values():
        info.append(objeto)
        suma_cantidad = int((sp.integrate(1, (x,0,objeto["cantidad_productos"])))) + int(suma_cantidad)
        cantidad.append([objeto['producto_id'],objeto["cantidad_productos"]])

    #Obtener los productos
    for conjunto_producto in Producto.objects.all():
        setattr(conjunto_producto, 'cantidad', 0)
        productos.append(conjunto_producto)

    for cantidad_producto in cantidad:
        for producto in productos:
            if cantidad_producto[0] == producto.id_producto:
                setattr(producto, 'cantidad', (producto.cantidad + cantidad_producto[1]))

    data = {
        'info' : info,
        'suma_cantidad' : suma_cantidad,
        'producto' : productos,
    }

    return render(request, "newList.html", data)

#Vista de la tabla general de los proveedores

@login_required
def lista_proveedores(request):
    data = {
        'proveedores' : Proveedores.objects.all(),
    }
    return render(request, "lista_proveedores.html", data)

#Vista de la página principal de calculo de incognitas para álgebra lineal

@login_required
def algebraLineal(request):
    return render(request, "operaciones.html")

#Vista de la página secundaria del calculo de incognitas para álgebra lineal

@login_required
def resultadoCalculo(request):
    x = [float(request.GET["x1"]), float(request.GET["x2"]), float(request.GET["x3"])]
    y = [float(request.GET["y1"]), float(request.GET["y2"]), float(request.GET["y3"])]
    z = [float(request.GET["z1"]), float(request.GET["z2"]), float(request.GET["z3"])]
    n = [float(request.GET["n1"]), float(request.GET["n2"]), float(request.GET["n3"])]
    data = {
        'm1' : request.GET["m1"],
        'm2' : request.GET["m2"],
        'm3' : request.GET["m3"],
        'p1' : request.GET["p1"],
        'p2' : request.GET["p2"],
        'p3' : request.GET["p3"],
        'x1' : request.GET["x1"],
        'x2' : request.GET["x2"],
        'x3' : request.GET["x3"],
        'y1' : request.GET["y1"],
        'y2' : request.GET["y2"],
        'y3' : request.GET["y3"],
        'z1' : request.GET["z1"],
        'z2' : request.GET["z2"],
        'z3' : request.GET["z3"],
        'n1' : request.GET["n1"],
        'n2' : request.GET["n2"],
        'n3' : request.GET["n3"],
        'resultadoX' : str(round(ecuacionlineal(x,y,z,n)[0],1)),
        'resultadoY' : str(round(ecuacionlineal(x,y,z,n)[1],1)),
        'resultadoZ' : str(round(ecuacionlineal(x,y,z,n)[2],1)),
    }
    return render(request,"resoperacion.html", data)

#Función utilizadas para las vistas

def ecuacionlineal(x,y,z,n):
    matriz = np.array([[x[0],y[0],z[0]],[x[1],y[1],z[1]],[x[2],y[2],z[2]]])
    matriz2 = np.array([n[0],n[1],n[2]])
    return lin.solve(matriz,matriz2)

def g_a_kg(valor):
    return valor / 1000
