from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^dashboard$', views.index),
    url(r'^info$', views.info),
    url(r'^register$', views.register),
    url(r'^new_listing$', views.listing),
]