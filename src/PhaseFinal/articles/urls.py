from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^create$', views.editWindow, name='create'),
    url(r'^save$', views.save, name='save'),

    url(r'^$', views.index, name='index'),
    url(r'^f(?P<find>.*)$', views.index, name='find'),
    url(r'^p(?P<page>[0-9]+)$', views.index, name='index'),
    url(r'^(?P<article_id>[0-9]+)$', views.read, name='read'),
    url(r'^(?P<article_id>[0-9]+)/update/$', views.update, name='update'),

]
