from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

# Create your models here.


class Customer(models.Model):
    # Customer models definition

    GENDER_TYPE = (
        ("M", _("Male")),
        ("F", _("Female")),
    )

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=100)
    address = models.CharField(max_length=64)
    genre = models.CharField(max_length=100, choices=GENDER_TYPE)
    age = models.CharField(max_length=12)
    city = models.CharField(max_length=32)
    zip_code = models.CharField(max_length=16)
    created_date = models.DateField(auto_now_add=True)
    save_by = models.ForeignKey(User, on_delete=models.PROTECT)

    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"

    def __str__(self):
        return self.name


class Invoice(models.Model):

    """
    Name=Invoice (facture) model definition
    Description:
    author: adamou@gmail.com

    """

    INVOICE_TYPE = (
        ("R", _("RECIEPT")),
        ("P", _("PROFORMA INVOICE")),
        ("I", _("INVOICE")),
    )

    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    invoice_date_time = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(decimal_places=2, default=0.0, max_digits=12)
    paid = models.BooleanField(default=False)
    last_updated_date = models.DateField(null=True, blank=True)
    invoice_type = models.CharField(max_length=1, choices=INVOICE_TYPE)
    comment = models.TextField(null=True, max_length=100, blank=True)
    save_by = models.ForeignKey(User, on_delete=models.PROTECT)

    class Meta:
        verbose_name = "Invoice"
        verbose_name_plural = "Invoices"

    def __str__(self) -> str:
        return f"{self.customer.name}_{self.invoice_date_time}"

    @property
    def get_total(self):
        articles = self.article_set.all()
        total = sum(article.get_total for article in articles)
        return total


class Article(models.Model):

    """
    Name=Article model definition
    Description:
    author: adamou@gmail.com

    """
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(
        decimal_places=2, default=0.0, max_digits=10)
    total = models.DecimalField(decimal_places=2, default=0.0, max_digits=10)

    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"

    @property
    def get_total(self):
        total = self.quantity * self.unit_price
        return total
