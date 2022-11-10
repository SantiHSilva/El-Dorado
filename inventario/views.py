from django.shortcuts import render
import numpy as np
import sympy as sp
from sympy.abc import x
import numpy.linalg as lin
from gestion.models import Informacion
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

def ecuacionlineal(x,y,z,n):
    matriz = np.array([[x[0],y[0],z[0]],[x[1],y[1],z[1]],[x[2],y[2],z[2]]])
    matriz2 = np.array([n[0],n[1],n[2]])
    return lin.solve(matriz,matriz2)


def inicial(request):
    return render(request,"base.html")

def menu2(request):
    return render(request,"menu_derecha.html", {"username": User.objects.all()})

@login_required
def buscar(request):
    return render(request,"busqueda.html")

@login_required
def algebraLineal(request):
    try:
        x = [float(request.GET["x1"]), float(request.GET["x2"]), float(request.GET["x3"])]
        y = [float(request.GET["y1"]), float(request.GET["y2"]), float(request.GET["y3"])]
        z = [float(request.GET["z1"]), float(request.GET["z2"]), float(request.GET["z3"])]
        n = [float(request.GET["n1"]), float(request.GET["n2"]), float(request.GET["n3"])]
        data = {
            'resultadoX' : str(round(ecuacionlineal(x,y,z,n)[0],1)),
            'resultadoY' : str(round(ecuacionlineal(x,y,z,n)[1],1)),
            'resultadoZ' : str(round(ecuacionlineal(x,y,z,n)[2],1)),
        }
        return render(request,"operaciones.html", data)
    except:
        return render(request, "operaciones.html")

def g_a_kg(valor):
    return valor / 1000

@login_required
def lista_completa(request):
    info = []
    suma_cantidad = 0
    suma_peso = 0
    for objeto in Informacion.objects.values():
        objeto["stock_reserva"] = int(objeto["cantidad_productos"]*0.2)
        info.append(objeto)
        suma_cantidad = int((sp.integrate(1, (x,0,objeto["cantidad_productos"])))) + int(suma_cantidad)
        if objeto["unidades"] == "2":
            suma_peso = g_a_kg((sp.integrate(1, (x,0,objeto["peso_unidad"])))) + suma_peso
        else:
            suma_peso = float((sp.integrate(1, (x,0,objeto["peso_unidad"])))) + suma_peso
    data = {
        'info' : info,
        'suma_cantidad' : suma_cantidad,
        'suma_peso' : round(suma_peso,2),
    }
    print(data["info"])
    return render(request,"lista_completa.html", data)

def debug(request):
    return(render(request,"exportTabla.html"))

@login_required
def resultado(request):
    if request.GET["prd"]:
        resultado = Informacion.objects.filter(nombre_descripcion__icontains=(request.GET["prd"]))
    try:
        return render(request, "resultado.html", {"name": request.GET["prd"], "info": resultado})
    except:
        return render(request, "resultado.html", {"name": ""})
