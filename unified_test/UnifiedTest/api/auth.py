from rest_framework import authentication
from django.shortcuts import get_object_or_404
from rest_framework import exceptions

from UnifiedTest.models import Page, PageAuthentication


class UnifiedPostAuth(authentication.BaseAuthentication):

    def try_basic_http_auth(self, request, page):
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

    def try_custom_headers(self, request, page):
        expected_header_name = page.authentication.value.split(':')[0]
        expected_header_value = page.authentication.value.split(':')[1]

        if not expected_header_name.startswith('HTTP'):
            expected_header_name = 'HTTP_%s' % expected_header_name

        received_header = request.META.get(expected_header_name, None)
        if not received_header:
            raise exceptions.AuthenticationFailed('Missing auth headers.')
        else:
            if expected_header_value == received_header:
                return
            else:
                msg = 'Invalid Credential Headers.'
                raise exceptions.AuthenticationFailed(msg)

    def authenticate(self, request):
        page_ref = request.parser_context['kwargs']['page_ref']
        page = get_object_or_404(Page, ref=page_ref)
        available_schemes = PageAuthentication.AUTH_CHOICES

        if page.authentication.type == available_schemes.Basic:
            self.try_basic_http_auth(request, page)
        elif page.authentication.type == available_schemes.Headers:
            self.try_custom_headers(request, page)
        elif page.authentication.type == available_schemes.OAuth:
            # TODO:
            return

