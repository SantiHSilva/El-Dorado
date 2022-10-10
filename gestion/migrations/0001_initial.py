# Generated by Django 4.1.2 on 2022-10-09 23:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Informacion',
            fields=[
                ('nombre_descripcion', models.CharField(max_length=255, verbose_name='Nombre y Descripción')),
                ('proveedor', models.CharField(max_length=255, verbose_name='Distribuidor')),
                ('direccion_proveedor', models.CharField(max_length=255, verbose_name='Dirección del pro.')),
                ('numero_proveedor', models.CharField(max_length=255, verbose_name='Número del contacto pro.')),
                ('fecha_modificacion', models.DateField(max_length=20, verbose_name='Fecha de modificacion')),
                ('fecha_vencimiento', models.DateField(max_length=20, verbose_name='Fecha aprox. de vencimiento')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('categoria_producto', models.CharField(max_length=100, verbose_name='Categoria del producto')),
                ('cantidad_productos', models.IntegerField(verbose_name='Cantidad actual')),
                ('stock_maximo', models.IntegerField(verbose_name='Stock minima')),
                ('stock_minimo', models.IntegerField(verbose_name='Stock maxima')),
                ('unidades', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name_plural': 'Información',
            },
        ),
    ]
