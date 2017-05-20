from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, reverse

from customauth.admin import UserCreationForm
from customauth.forms import UserLoginForm


def login_user(request):
    form = UserLoginForm(request.POST or None)

    print(form.is_valid())

    if form.is_valid():
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = authenticate(request, email=email, password=password)

        print(user)

        if user is not None:
            if user.is_active:
                login(request, user)

                if not hasattr(request, 'redirect_field_name'):
                    return redirect(reverse('channels:channels-list'))
                return redirect(request.redirect_field_name.next)

        else:
            form.add_error('password', u"Wrong password!")

    context = {
        "form": form,
    }
    return render(request, 'customauth/login.html', context)


def logout_user(request):
    logout(request)
    return redirect(reverse('customauth:login'))


def register_user(request):
    # form = UserRegisterForm(request.POST or None)
    form = UserCreationForm(request.POST or None)

    if form.is_valid():
        user = form.save(commit=False)

        # cleaned (normalized) data
        email = form.cleaned_data['email']
        password = form.cleaned_data["password1"]

        # user = super(UserCreationForm, form).save(commit=False)
        user.set_password(password)
        user.user_kind = form.cleaned_data['user_kind']

        # if new_email(user, email=email):
        user.save()

        # returns user object if creditionals are correct
        user = authenticate(request, email=email, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)

                if not hasattr(request, 'redirect_field_name'):
                    return redirect(reverse('customauth:login'))
                return redirect(request.redirect_field_name.next)

                # else:
                #    form.add_error('email', u"Such e-mail was registered earlier!")

    context = {
        "form": form,
    }
    return render(request, 'customauth/register.html', context)


def new_email(user, email):
    if User.objects.exclude(pk=user.pk).filter(email=email).exists():
        return False
    return True
