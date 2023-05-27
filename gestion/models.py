from django.db import models

# Create your models here.

#Clase para la creación de productos base

class Producto(models.Model):
    #Campos para la creación de productos base
    opciones_unidades = (('1', 'Kg'), ('2', 'g'), ('3', 'L'), ('4', 'Unidades'), ('5', 'Otros'))
    opciones_categoria = (('1', 'Alimentos y Bebidas'), ('2', 'Productos de limpieza'), ('3', 'Papeleria'), ('4', 'Salud'), ('5', 'Otros'))
    id_producto = models.AutoField(primary_key=True)
    nombre_descripcion = models.CharField(max_length = 255, verbose_name="Nombre y descripción")
    categoria_producto = models.CharField(max_length = 100, verbose_name="Categoria del producto", choices = opciones_categoria)
    unidades = models.CharField(max_length = 255, choices = opciones_unidades, verbose_name="Unidades")
    stock_maximo = models.IntegerField(verbose_name="Stock minima")
    stock_minimo = models.IntegerField(verbose_name="Stock maxima")
    def __str__(self):
        return self.nombre_descripcion

#Clase para la creación de subproductos

class Informacion(models.Model):
    class Meta:
        verbose_name_plural = 'Información'
    id = models.AutoField(primary_key=True)
    #   Relación de uno a muchos con la clase Producto
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, null=True)
    #   Campos de la clase
    proveedor =  models.CharField(max_length = 255, verbose_name="Proveedor")
    fecha_modificacion =  models.DateField(max_length = 20,verbose_name = "Fecha de modificación")
    fecha_vencimiento =  models.DateField(max_length = 20,verbose_name="Fecha de vencimiento")
    cantidad_productos = models.IntegerField(verbose_name="Cantidad actual")
    peso_unidad = models.FloatField(verbose_name="Peso por unidad")
    #El nombre para reflejarlo en la página, en este caso que muestre el nombre y descripción
    # def __str__(self):
    #     return self.producto

class Proveedores(models.Model):
    class Meta:
        verbose_name_plural = 'Proveedores'
    id = models.AutoField(primary_key=True)
    nombre_proveedor = models.CharField(max_length = 255, verbose_name="Nombre del proveedor")
    direccion_proveedor = models.CharField(max_length = 255, verbose_name="Dirección del proveedor")
    numero_proveedor = models.CharField(max_length = 255, verbose_name="Número del contacto del proveedor")
    correo_proveedor = models.CharField(max_length = 255, verbose_name="Correo del proveedor")
    dias_entrega_general = models.IntegerField(verbose_name="Días de entrega general")
    def __str__(self):
        return self.nombre_proveedor
    
class AuditoriaEntrada(models.Model):
    class Meta:
        verbose_name_plural = 'Auditoria'
    id = models.AutoField(primary_key=True)
    responsable = models.CharField(max_length = 255, verbose_name="Responsable")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Fecha y hora")
    producto = models.CharField(max_length = 255, verbose_name="Producto")
    cantidad = models.IntegerField(verbose_name="Cantidad")
    proveedor = models.CharField(max_length = 255, verbose_name="Proveedor")

class AuditoriaSalidas(models.Model):
    class Meta:
        verbose_name_plural = 'Auditoria'
    id = models.AutoField(primary_key=True)
    responsable = models.CharField(max_length = 255, verbose_name="Responsable")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Fecha y hora")
    producto = models.CharField(max_length = 255, verbose_name="Producto")
    cantidad = models.IntegerField(verbose_name="Cantidad")
    razon = models.CharField(max_length = 255, verbose_name="Razón")
    proveedor = models.CharField(max_length = 255, verbose_name="Proveedor")