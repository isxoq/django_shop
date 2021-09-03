from django.shortcuts import render
from .models import Category, Product
from django.core.exceptions import ObjectDoesNotExist
from django.utils import translation


# Create your views here.
def detail(request, slug):
    try:
        product = Product.objects.get(slug=slug)
        return render(request, 'product_detail.html', {
            'product': product
        })
    except ObjectDoesNotExist:
        pass


def index(request):

    categories = Category.objects.all()
    products = Product.objects.all().translate(translation.get_language())
    print(products[3].name)

    return render(request, 'index.html', {
        "categories": categories,
        "products": products
    })
