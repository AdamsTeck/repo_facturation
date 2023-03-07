from django.shortcuts import render
from django.views import View
from .models import *
from django.contrib import messages
from django.db import transaction
from .utiles import get_invoice
import datetime
from django.http import HttpResponse

import pdfkit

from django.template.loader import get_template

from django.core.paginator import (Paginator, EmptyPage, PageNotAnInteger)


# Create your views here.


class HomeView(View):
    # Main View

    templates_name = 'index.html'
    invoices = Invoice.objects.select_related(
        'customer', 'save_by').all().order_by('-invoice_date_time')

    context = {
        'invoices': invoices
    }

    def get(self, request, *args, **kwargs):

        # default_page
        default_page = 1
        page = request.GET.get('page', default_page)

        # pagination items
        items_per_page = 6

        paginator = Paginator(self.invoices, items_per_page)

        try:
            items_page = paginator.page(page)
        except PageNotAnInteger:
            items_page = paginator.page(default_page)
        except EmptyPage:
            items_page = paginator.page(paginator.num_pages)

        self.context['invoices'] = items_page

        return render(request, self.templates_name, self.context)

    def post(self, request, *args, **kwargs):

        # modify
        if request.POST.get('id_modified'):
            paid = request.POST.get('modified')

            try:
                obj = Invoice.objects.get(id=request.POST.get('id_modified'))
                if paid == 'True':
                    obj.paid = True
                else:
                    obj.paid = False
                obj.save()
                messages.success(request, "change made successfully.")
            except Exception as e:
                messages.error(
                    request, f"Sorry, the following error has occured {e} ")

         # deleting an invoice
        if request.POST.get('id_supprimer'):
            try:
                obj = Invoice.objects.get(pk=request.POST.get('id_supprimer'))
                obj.delete()
                messages.success(request, "The deleting was successfully.")
            except Exception as e:
                messages.error(
                    request, f"Sorry, the following error has occured {e} ")
        return render(request, self.templates_name, self.context)


class AddCustomerView(View):
    # add new customer
    template_name = 'add_customer.html'

    # Afficher le template add_customer.html
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    # Recuperer les valeurs
    def post(self, request, *args, **kwargs):

        data = {
            "name": request.POST.get("name"),
            "email": request.POST.get("email"),
            "phone": request.POST.get("phone"),
            "address": request.POST.get("address"),
            "genre": request.POST.get("genre"),
            "age": request.POST.get("age"),
            "city": request.POST.get("city"),
            "zip_code": request.POST.get("zip"),
            "save_by": request.user,
        }

        try:
            created = Customer.objects.create(**data)
            if created:
                messages.success(request, " Customer registered successuffly")
            else:
                messages.error(
                    request, "Sorry, please try again, the sent data is corrupt ")

        except Exception as e:
            messages.error(
                request, f"Sorry, our system is detecting the following issues {e}")
        # print(request.POST)
        return render(request, self.template_name)


class AddInvoiceView(View):

    # add a new invoice View

    template_name = "add_invoice.html"
    customers = Customer.objects.select_related('save_by').all()

    context = {
        'customers': customers
    }

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.context)

    # @transaction.atomic()
    def post(self, request, *args, **kwargs):

        items = []
        try:
            with transaction.atomic():
                customer = request.POST.get("customer")
                type = request.POST.get("invoice")
                articles = request.POST.getlist("article")
                qties = request.POST.getlist("qty")
                units = request.POST.getlist("unit")
                total_a = request.POST.getlist("total-a")
                total = request.POST.get("total")
                comment = request.POST.get("comment")

                invoice_objects = {
                    "customer_id": customer,
                    "save_by": request.user,
                    "total": total,
                    "invoice_type": type,
                    "comment": comment,
                }

                invoice = Invoice.objects.create(**invoice_objects)
                # Etant donné qu'on peut enregistrer plusieurs articles
                if articles and qties and units and total_a and total and comment:
                    for index, article in enumerate(articles):
                        data = Article(
                            invoice_id=invoice.id,
                            name=article,
                            quantity=qties[index],
                            unit_price=units[index],
                            total=total_a[index],
                        )
                        items.append(data)
                else:
                    messages.error(
                        request, "Please fill in all required fields.")

                # bulk_create créer en une fois un ensemble d'objects dans la bd
                created = Article.objects.bulk_create(items)
                if created:
                    messages.success(request, "Data saved successfully.")
                else:
                    messages.error(request, "Sorry, please try again")
        except Exception as e:
            messages.error(
                request, f"Sorry, our system is detecting the following issues {e}")
        print(request.POST)
        return render(request, self.template_name, self.context)


class InvoiceVieuw(View):

    template_name = "invoice.html"

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        context = get_invoice(pk)

        return render(request, self.template_name, context)

# function to download invoice in pdf


def get_invoice_download_pdf(request, *args, **kwargs):
    """generate pdf file from html file"""

    pk = kwargs.get('pk')
    context = get_invoice(pk)

    context['date'] = datetime.datetime.today()

    # get html file
    template = get_template('invoice_download_pdf.html')

    # render html with context variables
    html = template.render(context)

    # options of pdf format
    options = {
        'page-size': 'Letter',
        'encoding': 'UTF-8',
        'enable-local-file-access': '',
    }

    # generate pdf
    pdf = pdfkit.from_string(html, False, options)

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'

    return response
