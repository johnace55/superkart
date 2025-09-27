from product.models import Category
from django.conf import settings

def all_categories(request):

    categories = Category.objects.all()

    return dict(categories=categories)


def get_paypal_client_id(request):
    return {'PAYPAL_CLIENT_ID':settings.PAYPAL_CLIENT_ID}

