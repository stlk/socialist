from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.views.generic.base import View
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.conf import settings

from django_libretto.decorators import view_decorator
from instagram.client import InstagramAPI
from instagram import subscriptions

from .subscription_callback import reactor
from . import forms
from .models import Subscription

# access_token = request.user.social_auth.get().extra_data['access_token']

@view_decorator(login_required)
class SubscribeView(View):

    template_name = 'subscribe.html'

    def get(self, request):
        return render(request, self.template_name, {'form': forms.StreamForm()})

    def post(self, request):
        form = forms.StreamForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            subscription = Subscription(user=request.user)
            subscription.subscribe(data['tag'])
            return redirect('console:stream')
        else:
            return render(request, self.template_name, {'form': form})


def stream(request):
    return render(request, 'stream.html', {'user': request.user})


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
