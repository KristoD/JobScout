from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^signup$', views.register),
    url(r'^login$', views.login),
    url(r'^process/(?P<action>\w+)$', views.process),
    url(r'^user/(?P<ids>\d+)$', views.users),
    url(r'^user/(?P<id>\d+)/resume$', views.resume),
    url(r'^user/add/(?P<action>\w+)$', views.add),
    url(r'^user/(?P<id>\d+)/new/(?P<action>\w+)$', views.new),
    url(r'^user/(?P<id>\d+)/edit/(?P<action>\w+)$', views.edit_show),
    url(r'^user/edit/(?P<action>\w+)$', views.edit),
    url(r'^user/(?P<action>\w+)/(?P<id>\d+)/destroy$', views.destroy),
    url(r'^logout$', views.logout)
]