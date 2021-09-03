from django.db import models
from translations.models import Translatable
from django.utils import translation


# Create your models here.

class Translate(Translatable, models.Model):
    key = models.CharField(max_length=200)
    title = models.CharField(max_length=200)

    class TranslatableMeta:
        fields = ['title']

    # def __str__(self):
    #     return self.translate

    @staticmethod
    def t(key):
        return Translate.objects.get(key=key).title
