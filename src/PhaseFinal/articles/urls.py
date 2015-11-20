from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^f(?P<find>.*)$', views.find, name='find'),
    url(r'^p(?P<page>[0-9]+)$', views.index, name='index'),
    url(r'^(?P<article_id>[0-9]+)$', views.read, name='read'),
    url(r'^(?P<article_id>[0-9]+)/references/$', views.references, name='bibliography'),
]
