from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout, login
from django.core.urlresolvers import reverse

from django.http import HttpResponse
from django.conf import settings
from instagram.client import InstagramAPI
from instagram import subscriptions

from .subscription_callback import reactor
from . import forms
from .models import Subscription

# access_token = request.user.social_auth.get().extra_data['access_token']


def home_page(request):
    return render(request, 'home.html', {'form': forms.StreamForm()})


def subscribe(request):
    form = forms.StreamForm(request.POST)
    if form.is_valid():
        data = form.cleaned_data
        subscription = Subscription(user=request.user)
        subscription.subscribe(data['tag'])
        return redirect('console:stream')
    else:
        return render(request, 'home.html', {'form': form})


def stream(request):
    return render(request, 'stream.html', {'user': request.user})


def logout(request):
    """Logs out user"""
    auth_logout(request)
    unsubscribe()
    return redirect('/')


def unsubscribe():
    api = InstagramAPI(
        client_id=settings.SOCIAL_AUTH_INSTAGRAM_KEY,
        client_secret=settings.SOCIAL_AUTH_INSTAGRAM_SECRET)
    subscriptions = api.list_subscriptions()
    for subscription in subscriptions['data']:
        api.delete_subscriptions(id=subscription['id'])


def notification(request):
    mode = request.GET.get("hub.mode")
    challenge = request.GET.get("hub.challenge")
    verify_token = request.GET.get("hub.verify_token")
    if challenge:
        return HttpResponse(challenge)
    else:
        x_hub_signature = request.META.get('HTTP_X_HUB_SIGNATURE')
        raw_response = request.body.decode()
        try:
            reactor.process(settings.SOCIAL_AUTH_INSTAGRAM_SECRET, raw_response, x_hub_signature)
        except subscriptions.SubscriptionVerifyError:
            print("Signature mismatch")

    return HttpResponse()
