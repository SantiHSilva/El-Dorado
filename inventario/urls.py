"""inventario URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from gestion.views import FormularioInformacionView, exportResultadosPDF
from inventario import views
from django.conf import settings
from django.conf.urls.static import static

#Urls utilizadas en la página web

urlpatterns = [
    path('admin/', admin.site.urls),                                                   #Admin page
    path('', views.inicial),                                                           #Base page
    path('lista/', views.lista_completa),                                              #Lista de productos
    path('algebra/', views.algebraLineal),                                             #Calculo de incognitas
    path('resultado/', views.resultadoCalculo),                                        #Resultado del calculo de incognitas
    path('export/', exportResultadosPDF.as_view()),                                    #Exportar resultados a PDF
    path('modificar/<id>/', FormularioInformacionView.modificar_producto),             #Modificar información de un producto
    path('modificarbase/<id>/', FormularioInformacionView.modificar_base),             #Modificar producto base
    path('eliminarBase/<id>/', FormularioInformacionView.eliminar_productoBase),       #Eliminar producto base
    path('eliminarSubProducto/<id>/', FormularioInformacionView.eliminar_subProductos),#Eliminar información que tiene un producto base
    path('agregar/', FormularioInformacionView.agregar_producto),                      #Registrar productos base
    path('registrar/', FormularioInformacionView.index),                               #Registrar sub productos para productos base
]

if settings.DEBUG:  #Para poder ver las imagenes en el servidor de desarrollo                                             
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
