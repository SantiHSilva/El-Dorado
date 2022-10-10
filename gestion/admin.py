from django.contrib import admin

from gestion.models import Informacion

# Register your models here.

class moreInf(admin.ModelAdmin):
    list_display=("id", "nombre_descripcion", "cantidad_productos", "fecha_vencimiento")
    search_fields = ("id","nombre_descripcion")
    list_filter = ("fecha_modificacion","fecha_vencimiento","categoria_producto")

admin.site.register(Informacion, moreInf)

