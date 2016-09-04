from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^processform$', views.login),
    url(r'^process/login/(?P<id>\d+)$', views.loginsuccess, name='loginsuccess'),
    url(r'^process/logout$', views.logout, name="logout")
]
