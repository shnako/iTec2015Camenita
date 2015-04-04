from django.conf.urls import patterns, url

from UnifiedTest import api, views

urlpatterns = patterns('',
     url(r'^$', views.index, name='index'),
     url(r'^create/$', views.create_page, name='create-page'),
     url(r'^pages/$', views.pages, name='pages'),
     url(r'^requests/$', views.requests, name='requests'),
     url(r'^view/(?P<page_ref>.*)$', views.view_page_details, name='view-page'),
     url(r'^use/(?P<page_ref>.*)$', api.use_page, name='use-page'),
     url(r'^view/request-body/(?P<request_id>.*)$', views.view_request_details, name='view-request-body'),
     url(r'^view/response-body/(?P<request_id>.*)$', views.view_response_details, name='view-response-body'),
)
