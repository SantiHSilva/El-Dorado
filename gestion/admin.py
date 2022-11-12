from django.contrib import admin

from gestion.models import Informacion, Producto

# Register your models here.

class moreInf(admin.ModelAdmin):
    list_display=("id", "cantidad_productos", "producto")
    search_fields = ("id","nombre_descripcion")
    list_filter = ("fecha_modificacion","producto")

admin.site.register(Informacion, moreInf)
admin.site.register(Producto)

