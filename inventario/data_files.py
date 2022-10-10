# -*- coding: utf-8 -*-
import pprint
# from ..gestionInventario.models import Informacion

datas = []

def open_file():
    global head
    archivo = open("data/inventario.csv", "r") #read
    head = archivo.readline()
    head = head.replace("\n", "")
    head = head.split(",")
    head.sort()
    for line in archivo:
        line = line.replace("\n", "")
        line = line.split(",")
        d = {}
        j = 0
        for i in head:
            try:
                d[i] = int(line[j]) #convertir los datos númericos textuales a númericos
            except:
                d[i] = line[j]
            j = j + 1
        datas.append(d)
    #pprint.pprint(datas)
    archivo.close()
    return

def save_file(csv):
    archivo = open(f"data/{csv}.csv", "w") #write
    head = ",".join(datas[0])
    archivo.write(head + "\r")
    for line in datas:
        archivo.write(",".join(line.values()) + "\r")
    archivo.close()

def read_lines(csv):
    archivo = open(f"../static/data/{csv}.csv", "r")
    return len(archivo.readlines())

#ESTO VA SIEMPRE
# open_file("inventario")
#ESTO VA SIEMPRE

def searchElement(id):
    open_file()
    result = next((item for item in datas if item['id'] == id),{})
    return result

def printList(id):
    temp = searchElement(id)
    print(f"id: {temp['id']}") #se imprime la id primero
    for key, value in temp.items():
        if key != 'id': #no imprime la id
            print(f"{key}: {value}")

def deleteItem():
    temp = searchElement()
    

def modify():
    obj = searchElement()
    key = input("Ingrese el campo que desea modificar: ")
    value = input("Ingrese el valor para el campo: ")
    obj[key] = str(value)
    return obj

# def migrate():
#     for i in datas:
#         """"""
#         info_por_id = next(items for items in datas if items['id'] == i)
#         migrate = Informacion(nombre_descripcion = info_por_id.get('nombre_descripcion'))
#         migrate.save()

# migrate()
# result = modify
# pprint.pprint(result)
# # save_file("inventario")
# print(result.get('id')) #id





















def kerlon():
    sanchez = {"nombre":"hola",
                "XD": 2}
    print(sanchez['nombre']) 
    print(sanchez['XD']) 
    #nombre, apellido, cedula...
    registro = {
    "nombre": "Kerlon",
    "apellido": "Sanches",
    "cedula": 1070588505,
    "direccion": "transversal 23 #7c-04",
    }

    datos = [30]
    datos[0] = registro

    print(registro)

    # print(sanchez)