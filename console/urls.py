from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.SubscribeView.as_view(), name='subscribe'),
    url(r'^subscribed$', views.SubscribedView.as_view(), name='subscribed'),
]
