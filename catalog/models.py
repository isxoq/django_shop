from django.db import models


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50)
    icon = models.ImageField(upload_to="static_files/images/category")
    slug = models.CharField(max_length=50)
    parent_id = models.ForeignKey('Category', models.CASCADE, 'category_to_category_pk', blank=True, null=True)


class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    image = models.ImageField(upload_to="static_files/images/product")
    slug = models.CharField(max_length=50)
    category_id = models.ForeignKey('Category', models.CASCADE, 'category_to_product')
    old_price = models.IntegerField()
    price = models.IntegerField()
