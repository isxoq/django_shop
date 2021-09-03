from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Cart
from catalog.models import Product
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core import serializers
from .models import Order, OrderProduct
from .forms import OrderForm


# Create your views here.
@csrf_exempt
def add_to_cart(request):
    product_id = int(request.POST.get('product_id'))
    quantity = int(request.POST.get('quantity'))

    carts = Cart.objects.filter(user_id=request.user.id)

    product = Product.objects.get(id=product_id)

    try:
        cart = Cart.objects.get(product_id=product_id)
        cart.quantity += quantity
        cart.save()
    except ObjectDoesNotExist:
        cart = Cart.objects.create(product_id=Product.objects.get(id=product_id), quantity=quantity,
                                   user_id=User.objects.get(id=request.user.id))
        cart.save()
    return render(request, 'cart_data.html', {
        "carts": carts
    })


@csrf_exempt
def delete_from_cart(request):
    product_id = int(request.POST.get('product_id'))

    cart = Cart.objects.get(product_id=product_id)
    cart.delete()

    carts = Cart.objects.filter(user_id=request.user.id)

    return render(request, "checkout_table.html", {
        "carts": carts
    })


@login_required(login_url='/accounts/login')
def checkout(request):
    order_form = OrderForm()
    carts = Cart.objects.filter(user_id=request.user.id)

    if request.method == "POST":
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            order = Order()
            order.user_id = User.objects.get(id=request.user.id)
            order.phone = request.POST.get('phone')
            order.first_name = request.POST.get('first_name')
            order.last_name = request.POST.get('last_name')
            order.amount = get_cart_total_amount(request)
            order.save()

            save_order_products(order, request)

            clear_cart(request)
            return redirect('index')

    return render(request, 'checkout.html', {
        "form": order_form,
        "carts": carts,
        "total_amount": get_cart_total_amount(request)
    })


def get_cart_total_amount(request):
    carts = Cart.objects.filter(user_id=request.user.id)
    total = 0
    for cart in carts:
        total += cart.product_id.price * cart.quantity

    return total


def clear_cart(request):
    carts = Cart.objects.filter(user_id=request.user.id)
    carts.delete()


def save_order_products(order, request):
    carts = Cart.objects.filter(user_id=request.user.id)

    for cart in carts:
        order_product = OrderProduct()
        order_product.product_id = cart.product_id
        order_product.quantity = cart.quantity
        order_product.order_id = order.id
