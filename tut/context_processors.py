from product.models import Category

def all_categories(request):

    categories = Category.objects.all()

    return dict(categories=categories)




