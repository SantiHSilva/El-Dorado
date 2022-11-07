# from django.http import HttpResponse
# from django.template import Context, Library
from django.shortcuts import render
from gestion.models import Informacion
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

def modal(request):
    return render(request, "modal.html")

def inicial(request):
    return render(request,"base.html")

def menu2(request):
    return render(request,"menu_derecha.html", {"username": User.objects.all()})

@login_required
def buscar(request):
    return render(request,"busqueda.html")

@login_required
def lista_completa(request):
    info = []
    for objeto in Informacion.objects.values():
        objeto["stock_reserva"] = int(objeto["cantidad_productos"]*0.2)
        info.append(objeto)
    return render(request,"lista_completa.html", {"info": info})

@login_required
def eliminar_productos(request, id):
    producto = Informacion.objects.get(id=id)
    producto.delete()
    return redirect("/lista_completa")

@login_required
def resultado(request):
    if request.GET["prd"]:
        resultado = Informacion.objects.filter(nombre_descripcion__icontains=(request.GET["prd"]))
    try:
        return render(request, "resultado.html", {"name": request.GET["prd"], "info": resultado})
    except:
        return render(request, "resultado.html", {"name": ""})
