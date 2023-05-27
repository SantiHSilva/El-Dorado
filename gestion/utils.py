from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from enum import Enum
from .models import AuditoriaEntrada, AuditoriaSalidas

#Utils para renderizar páginas HTML a PDF

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

def guardar_entrada(nombre : str, producto : str, proveedor : str, cantidad : int):
    auditoria = AuditoriaEntrada()
    auditoria.responsable = nombre
    auditoria.producto = producto
    auditoria.cantidad = cantidad
    auditoria.proveedor = proveedor
    auditoria.save()
    # print(f'Entrada guardada: {nombre} {producto} {cantidad} {proveedor}')

def guardar_salida(nombre : str, producto : str, proveedor : str, cantidad : int, razon : str):
    auditoria = AuditoriaSalidas()
    auditoria.responsable = nombre
    auditoria.producto = producto
    auditoria.cantidad = cantidad
    auditoria.razon = razon
    auditoria.proveedor = proveedor
    auditoria.save()
