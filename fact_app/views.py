from django.shortcuts import render
from django.views import View
from .models import *
from django.contrib import messages
from django.db import transaction


# Create your views here.


class HomeView(View):
    # Main View

    templates_name = 'index.html'
    invoices = Invoice.objects.select_related('customer', 'save_by').all()

    context = {
        'invoices': invoices
    }

    def get(self, request, *args, **kwargs):
        return render(request, self.templates_name, self.context)

    def post(self, request, *args, **kwargs):
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
