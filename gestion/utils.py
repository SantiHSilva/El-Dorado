from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from enum import Enum
from .models import Auditoria

#Utils para renderizar páginas HTML a PDF

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

class acciones(Enum):
    ENTRADA = 1
    SALIDAS = 2

def guardar_entrada_salida(nombre, producto, acccion : acciones):
    auditoria = Auditoria()
    auditoria.user = nombre
    auditoria.model = acccion.name
    auditoria.accion = producto
    auditoria.save()
