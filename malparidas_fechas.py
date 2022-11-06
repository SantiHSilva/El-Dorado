
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






def suma ():
    a = int(input("Inserte un numero entero a sumar: "))
    b = int(input("Inserte el siguiente numero entero a sumar: "))
    operacion = a+b
    return operacion
    
print ("EL resultsdo de la suma es: " + str(suma()))





















