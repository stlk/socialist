from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.contrib.auth import logout as auth_logout


class LoginView(View):

    template_name = 'login.html'

    def get(self, request):
        return render(request, self.template_name)


def logout(request):
    """Logs out user"""
    auth_logout(request)
    return redirect('/')
