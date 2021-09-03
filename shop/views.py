from django.shortcuts import render, redirect
from translations.languages import translate
from django.utils import translation
from django.http import HttpResponseRedirect


def setlanguage(request, lang):
    translation.activate(lang)
    request.session['lang'] = lang
    return redirect('index')
