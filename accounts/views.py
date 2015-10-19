from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.contrib.auth import logout as auth_logout
from django.http import HttpResponse
from django.conf import settings

from instagram.client import InstagramAPI



class LoginView(View):

    template_name = 'login.html'

    def get(self, request):
        return render(request, self.template_name)


def logout(request):
    """Logs out user"""
    auth_logout(request)
    return redirect('/')


def unsubscribe(request):
    api = InstagramAPI(
        client_id=settings.SOCIAL_AUTH_INSTAGRAM_KEY,
        client_secret=settings.SOCIAL_AUTH_INSTAGRAM_SECRET)
    subscriptions = api.list_subscriptions()
    for subscription in subscriptions['data']:
        api.delete_subscriptions(id=subscription['id'])

    return HttpResponse()
