from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.home_page, name='home'),
    url(r'^stream$', views.stream, name='stream'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^subscribe$', views.subscribe, name='subscribe'),
    url(r'^notification$', views.notification, name='notification'),
]
