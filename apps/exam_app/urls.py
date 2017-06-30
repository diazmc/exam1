from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^process$', views.process),
    url(r'^login$', views.login),
    url(r'^appointments$', views.appointments),
    url(r'^addappointment$', views.addappointment),
    url(r'^appointments/(?P<id>\d+)$', views.editpage),
    url(r'^delete/(?P<id>\d+)$', views.delete),
    url(r'^update/(?P<id>\d+)$', views.update),
    url(r'^logout$', views.logout)
]