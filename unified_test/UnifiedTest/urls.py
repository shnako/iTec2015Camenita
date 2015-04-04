from django.conf.urls import patterns, url

from UnifiedTest import views
from UnifiedTest.api import views as api_views


urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^pages/$', views.pages, name='pages'),
                       url(r'^pages/create/$', views.create_page, name='create-page'),
                       url(r'^pages/(?P<page_ref>[0-9a-zA-Z\-]+)/$', views.edit_page, name='edit-page'),
                       url(r'^pages/(?P<page_ref>[0-9a-zA-Z\-]+)/delete/$', views.delete_page, name='delete-page'),
                       url(r'^pages/(?P<page_ref>[0-9a-zA-Z\-]+)/code/$', views.view_page_code, name='view-page-code'),
                       url(r'^pages/(?P<page_ref>[0-9a-zA-Z\-]+)/response/$', views.view_page_response, name='view-page-response'),
                       url(r'^requests/$', views.requests, name='requests'),
                       url(r'^use/(?P<page_ref>.*)/$', api_views.UsePage.as_view(), name='use-page'),
                       url(r'^view/request-body/(?P<request_id>.*)$', views.view_request_details, name='view-request-body'),
                       url(r'^view/response-body/(?P<request_id>.*)$', views.view_response_details, name='view-response-body'),
)
