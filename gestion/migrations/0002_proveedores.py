# Generated by Django 4.1.2 on 2023-05-20 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Proveedores',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_proveedor', models.CharField(max_length=255, verbose_name='Nombre del proveedor')),
                ('direccion_proveedor', models.CharField(max_length=255, verbose_name='Dirección del proveedor')),
                ('numero_proveedor', models.CharField(max_length=255, verbose_name='Número del contacto del proveedor')),
                ('correo_proveedor', models.CharField(max_length=255, verbose_name='Correo del proveedor')),
                ('dias_entrega_general', models.IntegerField(verbose_name='Días de entrega general')),
            ],
            options={
                'verbose_name_plural': 'Proveedores',
            },
        ),
    ]
