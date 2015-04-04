from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone

from UnifiedTest.models import Page, PageAccessLog, HTTP_METHODS, PageAuthentication


class UsePage(APIView):

    def _get_page(self, page_ref):
        return get_object_or_404(Page, ref=page_ref)

    # TODO Verify user is owner
    def _create_acces_log_entry(self, request, page, request_type):
        PageAccessLog.objects.create(page=page, timestamp=timezone.now(),
                                     request_type=request_type,
                                     request_body=dict(request.data),
                                     response_body='Ana are mere')
        # TODO: compile the response body

    def get(self, request, page_ref, format=None):
        page = self._get_page(page_ref)
        self._create_acces_log_entry(request, page, HTTP_METHODS.GET)

        return Response()

    def put(self, request, page_ref, format=None):
        self._create_acces_log_entry(request ,page_ref, HTTP_METHODS.PUT)

        return Response()

    def post(self, request, page_ref, format=None):
        self._create_acces_log_entry(request, page_ref, HTTP_METHODS.POST)

        return Response()

    def delete(self, request, page_ref, format=None):
        self._create_acces_log_entry(request, page_ref, HTTP_METHODS.DELETE)

        return Response()

def delete_page(request, page_ref):
    page = get_object_or_404(Page, ref=page_ref)

    try:
        page.access_logs.all().delete()
    except:
        # No access logs, no worries.
        pass

    page.authentication.delete()
    page.delete()

    # Confirm with a 200 OK.
    return Response()