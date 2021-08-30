from django.contrib import admin
from django.urls import path, include
from order import views

urlpatterns = [
    path('add-to-cart', views.add_to_cart, name="add_to_cart"),
    path('delete-from-cart', views.delete_from_cart, name="delete_from_cart"),
    path('checkout', views.checkout, name="checkout")
]
