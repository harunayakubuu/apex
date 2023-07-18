from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from sales.models import Sale

# xhtml2pdf imports
import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders


class SaleListView(ListView):
    model = Sale
    template_name = 'invoices/main.html'


def sales_render_pdf(request, *args, **kwargs):
    pk = kwargs.get('pk')
    sale = get_object_or_404(Sale)

    template_path = 'invoices/pdf2.html'
    context = {'sale': sale}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    # If download
    # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    # If display
    response['Content-Disposition'] = 'filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
    #    html, dest=response, link_callback=link_callback)
       html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
    

def render_pdf_view(request):
    template_path = 'invoices/invoices.html'
    context = {'myvar': 'this is your template context'}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    # If download
    # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    # If display
    response['Content-Disposition'] = 'filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
    #    html, dest=response, link_callback=link_callback)
       html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response