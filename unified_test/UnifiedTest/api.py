import time

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.conf import settings

from UnifiedTest.models import Page, PageAccessLog, HTTP_METHODS, PageAuthentication



class UsePage(APIView):

    def _get_page(self, page_ref):
        return get_object_or_404(Page, ref=page_ref)

    def _attach_dynamic_method(self, code):
        method_name = getattr(settings, 'DEFAULT_DYNAMIC_METHOD_NAME', 'fun')
        context = {}
        exec code.strip() in context
        setattr(self.__class__, method_name, context[method_name])

        return context[method_name]

    def _handle_request(self, request, request_method, page_ref, dynamic_code):
        page = self._get_page(page_ref)
        log_item = PageAccessLog.objects.create(page=page, timestamp=timezone.now(),
                                                request_method=request_method,
                                                request_body=dynamic_code)

        if page.default_response == Page.DEFAULT_RESPONSES.Static:
            response_body = page.response
        elif page.default_response == Page.DEFAULT_RESPONSES.Dynamic:
            if not dynamic_code:
                dynamic_code = page.dynamic_code
            if dynamic_code:
                method = self._attach_dynamic_method(dynamic_code)
                response_body = method(self, request)
            else:
                response_body = ''

        time.sleep(page.delay/1000)

        log_item.response_body = response_body
        log_item.save()

        return Response(data=response_body, status=page.status_code)

    def get(self, request, page_ref, format=None):
        code = request.query_params.get('code', '')
        return self._handle_request(request, HTTP_METHODS.GET, page_ref, code)

    def put(self, request, page_ref, format=None):
        code = request.data.get('code', '')
        return self._handle_request(request, HTTP_METHODS.PUT, page_ref, code)

    def post(self, request, page_ref, format=None):
        code = request.data.get('code', '')
        return self._handle_request(request, HTTP_METHODS.PUT, page_ref, code)

    def delete(self, request, page_ref, format=None):
        code = request.data.get('code', '')
        return self._handle_request(request, HTTP_METHODS.PUT, page_ref, code)

def delete_page(request, page_ref):
    page = get_object_or_404(Page, ref=page_ref)

    try:
        page.access_logs.all().delete()
    except:
        # No access logs, no worries.
        pass

    page.authentication.delete()
    page.delete()

    messages.success(request, 'The page has been deleted.')
    return Response()
>>>>>>> 560c98fc0a85b76b4ee710d31dc775624416a10a
