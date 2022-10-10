from django.template import Library
from django.utils.safestring import mark_safe
from datetime import datetime
import time

register = Library()

@register.filter(name="calcular_vencimiento")
def calcular_vencimiento(fecha):

    #now date in timestamp

    now = datetime.now()
    now = time.mktime(now.timetuple())

    #fecha de vencimiento en timestamp

    dia_vencimiento = time.mktime(fecha.timetuple())

    print(f"Dia vencimiento: {dia_vencimiento}" )

    print(f"Dia: {now}" )

    color = "color: red;"

    if((dia_vencimiento-now ) >= 864000):
        return mark_safe(f"<td>{fecha}</td>") # no vence ahora
    else:
        return mark_safe(f'<td style="{color}">{fecha}</td>') #si vence en el lapso de 10 días



