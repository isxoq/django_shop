from django.contrib import admin
from translations.admin import TranslatableAdmin, TranslationInline
from .models import Translate


# Register your models here.

class TranslateAdmin(TranslatableAdmin):
    inlines = [TranslationInline, ]


admin.site.register(Translate, TranslateAdmin)
