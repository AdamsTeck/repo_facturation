from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('add-customer', views.AddCustomerView.as_view(), name='add-customer'),
    path('add-invoice', views.AddInvoiceView.as_view(), name='add-invoice'),
    path('statistic', views.StatisticView.as_view(), name='statistic'),
    path('view-invoice/<int:pk>', views.InvoiceVieuw.as_view(), name='view-invoice'),
    path('pdf-download-invoice/<int:pk>', views.get_invoice_download_pdf, name='pdf-download-invoice'),
]


