from django.template import Library
from django.utils.safestring import mark_safe
from datetime import datetime
import time

register = Library()

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

@register.filter(name="calcular_vencimiento")
def calcular_vencimiento(fecha):
    print(type(fecha))
    print(fecha)
    date_now = datetime.now()
    fmt = "%Y-%m-%d %H:%M:%S"
    now = time.mktime(date_now.timetuple())
    # fecha = fecha + " 00:00:00"
    # fecha = datetime.strptime(str(fecha), fmt)
    fecha_vencimiento = time.mktime(fecha.timetuple())
    date_venc = datetime.fromtimestamp(fecha_vencimiento)
    print("Fecha de hoy: " + str(date_now))
    print("Fecha ingresada: " + str(date_venc))
    dia_vencimiento = datetime.strptime(str(date_venc), fmt)
    color = "color: red;"
    if((fecha_vencimiento-now ) >= 864000):
        return mark_safe(f"<td title= Aun no vence, le queda {(date_now - dia_vencimiento).days} días para que caduque" +">{transform_date(str(fecha))}</td>") # no vence ahora
    else:
        if ((date_now - dia_vencimiento).days) > 10:
            return mark_safe(f'<td style="{color}" title="Ya venció, venció hace {(date_now - dia_vencimiento).days} días"">{transform_date(str(fecha))}</td>') #si vence en el lapso de 10 días
        else:
            return mark_safe(f'<td style="{color}" title="Vence en {abs((date_now - dia_vencimiento).days)} días"">{transform_date(str(fecha))}</td>')



