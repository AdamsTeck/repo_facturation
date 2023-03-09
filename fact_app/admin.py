from django.contrib import admin
from .models import *

from django.utils.translation import gettext_lazy as _

# Register your models here.


class AdminCustomer(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'address',
                    'genre', 'age', 'city', 'zip_code')


class AdminInvoice(admin.ModelAdmin):
    list_display = ('customer', 'save_by', 'invoice_date_time',
                    'total', 'last_updated_date', 'paid', 'comment')


class AdminArticle(admin.ModelAdmin):
    list_display = ('invoice', 'name', 'quantity', 'unit_price', 'total')


admin.site.register(Customer, AdminCustomer)
admin.site.register(Invoice, AdminInvoice)
admin.site.register(Article, AdminArticle)

admin.site.site_title = _("ADAMS INVOICE SYSTEM")
admin.site.site_header = _("ADAMS INVOICE SYSTEM")
admin.site.index_title = _("ADAMS INVOICE SYSTEM")
