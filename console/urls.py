from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.SubscribeView.as_view(), name='subscribe'),
    url(r'^stream$', views.stream, name='stream'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^notification$', views.notification, name='notification'),
]
