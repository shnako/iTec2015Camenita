from django.conf.urls import patterns, url
from user_management import views

urlpatterns = patterns('',
                       url(r'^login/$', views.login_user, name='login'),
                       url(r'^register/$', views.register, name='create-user'),
                       url(r'^logout-user/$', views.logout_user, name='logout-user')
)