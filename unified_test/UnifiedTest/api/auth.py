from rest_framework import authentication
from django.shortcuts import get_object_or_404
from rest_framework import exceptions

from UnifiedTest.models import Page, PageAuthentication


class UnifiedPostAuth(authentication.BaseAuthentication):

    def _try_basic_http_auth(self, request, page):
        auth_header = request.META.get('HTTP_AUTHORIZATION', None)
        if not auth_header:
            raise exceptions.AuthenticationFailed('Missing auth headers.')
        else:
            auth_header_value = auth_header.replace('Basic ', '')
            if page.authentication.value == auth_header_value:
                return
            else:
                msg = 'Invalid Basic HTTP credentials.'
                raise exceptions.AuthenticationFailed(msg)

    def authenticate(self, request):
        page_ref = request.parser_context['kwargs']['page_ref']
        page = get_object_or_404(Page, ref=page_ref)
        available_schemes = PageAuthentication.AUTH_CHOICES

        if page.authentication.type == available_schemes.Basic:
            self._try_basic_http_auth(request, page)
