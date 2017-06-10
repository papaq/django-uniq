from django import forms


class MessageForm(forms.Form):
    message = forms.CharField(max_length=2000, required=True)
