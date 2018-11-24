from django import forms
from django.contrib.auth.models import User
from .models import Token
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class TokenForm(forms.ModelForm):
	class Meta:
		model = Token
		fields = "__all__"