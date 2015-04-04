from django.conf.urls import patterns, url

from UnifiedTest import views
from UnifiedTest import api as api_views


urlpatterns = patterns('',
     url(r'^$', views.index, name='index'),
     url(r'^create/$', views.create_page, name='create-page'),
     url(r'^pages/$', views.pages, name='pages'),
     url(r'^requests/$', views.requests, name='requests'),
     url(r'^view/page/(?P<page_ref>[a-zA-Z\-])/$', views.view_page_details, name='view-page'),
     url(r'^view/page/(?P<page_ref>.*)/response/$', views.view_page_response, name='view-page-response'),
     url(r'^view/page/(?P<page_ref>.*)/code/$', views.view_page_code, name='view-page-code'),
     url(r'^use/(?P<page_ref>.*)/$', api_views.UsePage.as_view(), name='use-page'),
     url(r'^view/request-body/(?P<request_id>.*)$', views.view_request_details, name='view-request-body'),
     url(r'^view/response-body/(?P<request_id>.*)$', views.view_response_details, name='view-response-body'),
)
