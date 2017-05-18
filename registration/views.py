from django.contrib.auth.models import User
from django.forms.utils import ErrorList
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from django.views.generic import View
from .user_form import UserRegisterForm


def login_user(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                #albums = Album.objects.filter(user=request.user)
                return render(request, 'channels/base.html')
            #else:
            #    return render(request, 'registration/login.html', {'error_message': 'Your account has been disabled'})
        else:

            return render(request, 'registration/login.html', {'error_message': 'Invalid login'})
    return render(request, 'registration/login.html')


def logout_user(request):
    logout(request)
    form = UserRegisterForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'channels/base.html', context)


def register(request):
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():

        user = form.save(commit=False)

        # cleaned (normalized) data
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']

        if new_email(user, email=email):

            user.set_password(password)
            user.save()

            # returns user object if creditionals are correct
            user = authenticate(request, email=email, password=password)

            if user is not None:

                if user.is_active:
                    login(request, user)
                    return redirect(request.redirect_field_name.next)

        else:
            form.add_error('email', u"Such e-mail already exists!")

    context = {
        "form": form,
    }

    return render(request, 'registration/registration_form.html', context)


def new_email(user, email):
    if User.objects.exclude(pk=user.pk).filter(email=email).exists():
        return False
    return True

