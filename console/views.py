from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.views.generic.base import View
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from django_libretto.decorators import view_decorator
from instagram.client import InstagramAPI
from instagram import subscriptions

from .subscription_callback import reactor
from . import forms
from .models import Subscription



@view_decorator(login_required)
class SubscribeView(View):

    template_name = 'subscribe.html'

    def get(self, request):
        try:
            request.user.subscription
            return redirect('console:stream')
        except ObjectDoesNotExist:
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


@view_decorator(login_required)
class StreamView(View):

    template_name = 'stream.html'

    def get(self, request):
        return render(request, self.template_name, {'user': request.user})


    def post(self, request):
        api = InstagramAPI(
            client_id=settings.SOCIAL_AUTH_INSTAGRAM_KEY,
            client_secret=settings.SOCIAL_AUTH_INSTAGRAM_SECRET)

        subscription = Subscription.objects.get(user=request.user)
        api.delete_subscriptions(id=subscription.instagram_id)
        subscription.delete()
        return redirect('console:subscribe')


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
