from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'(?P<id>\d+)$', views.listing),
    url(r'application/(?P<id>\d+)/process$', views.application_process),
]