from django.conf.urls import patterns, url
from UnifiedTest import views

urlpatterns = patterns('',
                       url(r'^login/$', views.Login, name='login'),
)