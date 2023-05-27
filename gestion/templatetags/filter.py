from django.template import Library
from django.utils.safestring import mark_safe
from datetime import datetime
import time

register = Library()

@register.simple_tag
def sumatoriaUnidades(value, unidades, categoria):
    return (template_g_a_kg(value, unidades, categoria))

@register.simple_tag
def observerNumber(cantidad, stock_maximo, stock_minimo):
    # print(f'Cantidad: {cantidad} Stock minimo: {stock_minimo} Stock maximo: {stock_maximo}')
    if cantidad < stock_minimo:
        return mark_safe(f'<td style="color: red; text-decoration: underline;" title="Cantidad menor al stock mínimo">{cantidad}</td>')
    elif cantidad > stock_maximo:
        return mark_safe(f'<td style="color: #fc7303; text-decoration: underline;" title="Cantidad mayor al stock máximo">{cantidad}</td>')
    else:
        return mark_safe(f'<td style="color: black;" title="Cantidad dentro del rango">{cantidad}</td>')

@register.filter(name='transform_unidades')
def transform_unidades(unidades):
    return (template_unidades(unidades))

@register.filter(name="transform_categoria")
def transform_categoria(categoria):
    return (template_categoria(categoria))

@register.filter(name="calcular_vencimiento")
def calcular_vencimiento(fecha):
    return (templateVencimiento(fecha))

@register.filter(name="motivo")
def convert_motivo(number):
    return (convert_motivo(int(number)))

def convert_motivo(number):
    match number:
        case 1:
            return "Consumo"
        case 2:
            return "Dañado"
        case 3:
            return "Donación"
        case _:
            return "Otros"

def template_g_a_kg(value, unidades, categoria):
    if unidades == "1":
        return (f'{round(value,2)}kg')
    if unidades == "2":
        if categoria == "2":
            return(f'{round(value/1000,2)}kg/m³')
        return (f"{round(value / 1000,2)}kg")
    if unidades == "3":
        return(f'{round(value,2)}kg/m³')
    if unidades == "4":
        return(f'{round(value,2)}u')
    else:
        return round(value,2)

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

def template_unidades(unidades):
    match unidades:
        case "1":
            return "Kilogramos"
        case "2":
            return "Gramos"
        case "3":
            return "Litros"
        case "4":
            return "Unidades"
        case _:
            return "Otros"
    
def template_categoria(categoria):
    match categoria:
        case "1":
            return "Alimentos y Bebidas"
        case "2":
            return "Limpieza"
        case "3":
            return "Papeleria"
        case "4":
            return "Salud"
        case _:
            return "Otros"

def templateVencimiento(fecha):
    date_now = datetime.now()
    fmt = "%Y-%m-%d %H:%M:%S"
    now = time.mktime(date_now.timetuple())
    fecha_vencimiento = time.mktime(fecha.timetuple())
    date_venc = datetime.fromtimestamp(fecha_vencimiento)
    dia_vencimiento = datetime.strptime(str(date_venc), fmt)
    vencio = "color: red;"
    por_vencer = "color: #fc7303;"
    if((fecha_vencimiento-now ) >= 864000):
        return mark_safe(f'<td style="color: black;" title="Aun no vence, le queda {abs(date_now - dia_vencimiento).days} días para que caduque">{transform_date(str(fecha))}</td>') # no vence ahora
    else:
        if ((date_now - dia_vencimiento).days) > 10:
            return mark_safe(f'<td style="{vencio}" title="Ya venció, venció hace {(date_now - dia_vencimiento).days} días"">{transform_date(str(fecha))}</td>') #si vence en el lapso de 10 días
        else:
            return mark_safe(f'<td style="{por_vencer}" title="Vence en {abs((date_now - dia_vencimiento).days)} días"">{transform_date(str(fecha))}</td>')

