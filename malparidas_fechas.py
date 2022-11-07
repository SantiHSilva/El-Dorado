
from datetime import datetime
import time

now = datetime.now()
def transform_date(fecha):
    ano = (fecha[0:4])
    mes = (fecha[5:7])
    dia = (fecha[8:10])
    if mes == "01":
        mes = "Enero"
    elif mes == "02":
        mes = "Febrero"
    elif mes == "03":
        mes = "Marzo"
    elif mes == "04":
        mes = "Abril"
    elif mes == "05":
        mes = "Mayo"
    elif mes == "06":
        mes = "Junio"
    elif mes == "07":
        mes = "Julio"
    elif mes == "08":
        mes = "Agosto"
    elif mes == "09":
        mes = "Septiembre"
    elif mes == "10":
        mes = "Octubre"
    elif mes == "11":
        mes = "Noviembre"
    elif mes == "12":
        mes = "Diciembre"
    return dia + " de " + mes + " de " + ano

# print(transform_date(str(now)))


def calcular_vencimiento(fecha):
    date_now = datetime.now()
    fmt = "%Y-%m-%d %H:%M:%S"
    now = time.mktime(date_now.timetuple())
    fecha = fecha + " 00:00:00"
    fecha = datetime.strptime(str(fecha), fmt)
    fecha_vencimiento = time.mktime(fecha.timetuple())
    date_venc = datetime.fromtimestamp(fecha_vencimiento)
    print("Fecha de hoy: " + str(date_now))
    print("Fecha ingresada: " + str(date_venc))
    tstamp2 = datetime.strptime(str(date_venc), fmt)
    if((fecha_vencimiento-now) >= 864000): #Lapso de 10 días
        print(f"Aun no vence, le queda {(date_now - tstamp2).days} días para que caduque") # no vence ahora
    else:
        if ((date_now - tstamp2).days) > 10:
            print(f"Ya venció, venció hace {(date_now - tstamp2).days} días")
        else:
            print(f"¡Le quedan {(date_now - tstamp2).days} días para que caduque!") #si vence en el lapso de 10 días

# calcular_vencimiento("2005-04-10")

#función declarada

def suma(a,b):
    return str(a+b)

print("La suma entre los valores es: " + suma(1,3))

def 











import os

a = 1
i = 0

def separar(a):
    return ("{:2}".format(a))

os.system("cls")
while a != 0:
    while ((a>10) or (a<0)) or (a!=0):
        try:
            a = int(input("Ingresa un número entre 1 y 10: "))
        except:
            print("Ingresa un número válido")
    if a == 0:
        break
    print()
    if a == 1:
        for i in range(11):
            print(f"1 * {separar(i)} = {separar(i)}     2 * {separar(i)} = {separar(2*i)}")
    elif a == 10:
        for i in range(11):
            print(f"9 * {separar(i)} = {separar(9*i)}     10 * {separar(i)} = {separar(10*i)}")
    else:
        for i in range(11):
            print(str(a-1) + "*" + str(i) + "=" + str((a-1)*i) + str(a)+" * "str(i)+"=" str(a*i)+str(a+1)+" * "+ str(i)+ "=" + str((a+1)*i))
        input("\nPresiona enter para continuar")

os.system("cls")
print("Fin del programa")
