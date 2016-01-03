from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.contrib.auth.decorators import login_required

from django_libretto.decorators import view_decorator

from . import forms
from .models import Subscription
from .instagram import Instagram


@view_decorator(login_required)
class SubscribeView(View):

    template_name = 'subscribe.html'

    def get(self, request):
        if Subscription.is_user_subscribed(request.user):
            return redirect('console:subscribed')
        else:
            return render(request, self.template_name, {'form': forms.SubscribeForm()})

    def post(self, request):
        form = forms.SubscribeForm(request.POST)

        if Instagram(request.user).user_has_no_posts():
            form.add_error('email', "We can't handle users with no posts, sorry.")

        if form.is_valid():
            data = form.cleaned_data
            Subscription.subscribe(request.user, data['email'])
            return redirect('console:subscribed')
        else:
            return render(request, self.template_name, {'form': form})


@view_decorator(login_required)
class SubscribedView(View):

    template_name = 'subscribed.html'

    def get(self, request):
        return render(request, self.template_name, {'user': request.user})

    def post(self, request):
        Subscription.unsubscribe(request.user)
        return redirect('console:subscribe')
