from django.shortcuts import render
from django.views import View
from .models import *
from django.contrib import messages

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
    # add nw customer
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
