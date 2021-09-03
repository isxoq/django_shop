# Created By Isxoqjon Axmedov
# ninja.uz
# https://t.me/isxoqjon
# +998936448111

from django.utils import translation


class LanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        if 'lang' not in request.session:
            request.session['lang'] = 'ru'
        translation.activate(request.session['lang'])
        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
