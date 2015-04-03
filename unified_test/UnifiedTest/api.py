from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone

from UnifiedTest.models import Page, PageAccessLog, HTTP_METHODS

class UsePage(APIView):

    def _create_acces_log_entry(self, ref_page, request_type):
        page = get_object_or_404(Page, ref=page_ref)
        PageAccessLog.objects.create(page=page, timestamp=timezone.now(),
                                     request_type=request_type,
                                     request_body=request.data,
                                     response_body='Ana are mere')
        # TODO: compile the response body

    def get(self, request, page_ref, format=None):
        self._create_acces_log_entry(ref_page, HTTP_METHODS.GET)

        return Response()

    def put(self, request, page_ref, format=None):
        self._create_acces_log_entry(ref_page, HTTP_METHODS.PUT)

        return Response()

    def post(self, request, page_ref, format=None):
        self._create_acces_log_entry(ref_page, HTTP_METHODS.POST)

        return Response()

    def delete(self, request, page_ref, format=None):
        self._create_acces_log_entry(ref_page, HTTP_METHODS.DELETE)

        return Response()
