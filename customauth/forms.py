from django import forms
from django.contrib.auth import get_user_model


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


class UserSubscriptionForm(forms.Form):
    search_request = forms.CharField(max_length=255, required=True)


class UserChoiceForm(forms.Form,):
    choice = forms.ChoiceField(required=False)

    def __init__(self, *args, **kwargs):
        choices = kwargs.pop('choices', [])
        super(UserChoiceForm, self).__init__(*args, **kwargs)
        self.fields['choice'].choices = choices
