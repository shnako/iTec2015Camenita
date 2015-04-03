from django.conf.urls import patterns, url
from UnifiedTest import views

urlpatterns = patterns('',
     url(r'^login/$', views.login, name='login'),
     url(r'^$', views.index, name='index'),
     url(r'^create/$', views.create_page, name='create-page'),
     url(r'^view/(?P<page_id>.*)$', views.view_page_details, name='view-page'),
     url(r'^use/(?P<page_uuid>.*)$', views.use_page, name='use-page'),
)
