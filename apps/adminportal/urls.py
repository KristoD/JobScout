from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'dashboard$', views.dashboard),
    url(r'^$', views.login),
    url(r'process/(?P<action>\w+)$', views.process),
    url(r'user/(?P<id>\d+)$', views.user),
    url(r'employer/(?P<id>\d+)$', views.employer),
    url(r'unban/(?P<id>\d+)/(?P<action>\w+)$', views.unban),
    url(r'ban/(?P<id>\d+)/(?P<action>\w+)$', views.ban)
]