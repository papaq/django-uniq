from django.contrib.auth.models import User
from django import forms


class UserRegisterForm(forms.ModelForm):

    USER_TYPES = (
        ('S', 'Student'),
        ('T', 'Teacher'),
        ('A', 'Assistant'),
    )

    user_type = forms.ChoiceField(choices=USER_TYPES, required=True)
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(max_length=255, required=True)
    # password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'user_type', ]
