from .models import *


def get_invoice(pk):
    # **kwargs est un dictionnaire infini

    obj = Invoice.objects.get(pk=pk)

    articles = obj.article_set.all()
    context = {
        'obj': obj,
        'articles': articles
    }
    return context
