from django.contrib import admin
from .models import Category, Product
from translations.admin import TranslatableAdmin, TranslationInline


# Register your models here.

class ProductAdmin(TranslatableAdmin):
    inlines = [TranslationInline, ]


admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
