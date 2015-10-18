import django.forms

class StreamForm(django.forms.Form):
	tag = django.forms.CharField()
