import django.forms

class SubscribeForm(django.forms.Form):
	email = django.forms.CharField()
