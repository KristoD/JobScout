from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'dashboard$', views.index),
    url(r'company/(?P<id>\d+)$', views.company),
    url(r'signin$', views.login),
    url(r'signup$', views.register),
    url(r'add/(?P<action>\w+)$', views.add),
    url(r'company/(?P<id>\d+)/edit/(?P<action>\w+)$', views.edit_company),
    url(r'edit/(?P<action>\w+)$', views.edit),
    url(r'company/(?P<id>\d+)/listings$', views.listings),
    url(r'company/(?P<id>\d+)/new/listing$', views.new_listing),
    url(r'process/(?P<action>\w+)$', views.process),
    url(r'new_listing$', views.listing),
]