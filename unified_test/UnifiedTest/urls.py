from django.conf.urls import patterns, url

from UnifiedTest import views
from UnifiedTest.api import UsePage

urlpatterns = patterns('',
     url(r'^$', views.index, name='index'),
     url(r'^create/$', views.create_page, name='create-page'),
     url(r'^view/(?P<page_ref>.*)$', views.view_page_details, name='view-page'),
     url(r'^use/(?P<page_ref>.*)$', UsePage.as_view(), name='use-page'),
)
