from django import forms
from django.contrib.auth import get_user_model
from random import randrange


class UserLoginForm(forms.Form):
    email = forms.EmailField(max_length=255)
    password = forms.CharField(widget=forms.PasswordInput)


class UserProfileForm(forms.ModelForm):

    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'avatar')

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name').title()
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name').title()
        return last_name

