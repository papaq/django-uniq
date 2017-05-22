from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, reverse

from channels.models import Group
from customauth.admin import UserCreationForm
from customauth.forms import UserLoginForm


def login_user(request):
    form = UserLoginForm(request.POST or None)

    if form.is_valid():
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = authenticate(request, email=email, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)

                if not hasattr(request, 'next'):
                    return redirect(reverse('channels:channels-list'))
                return redirect(request.next)

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


@login_required
def profile(request):
    form = UserCreationForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        pass

    context = {
        'form': form,
    }
    return render(request, 'customauth/profile.html', context)

    return render(request, 'customauth/profile.html', context)


def get_student_channel(user):
    user = user
    user_kind = user.user_kind
    context = {
        'university': None,
        'faculty': None,
        'group': None,
    }

    if user_kind == 'student':
        context = get_student_channel(user)
    else:
        if user_kind == 'academic':
            context = get_academic_channel(user)
        else:
            if user_kind == 'staff':
                context = get_staff_channel(user)

    context = {
        'university': None,
        'faculty': None,
        'group': None,
    }

    return context


def get_academic_channel(user):
    context = {
        'university': None,
        'faculty': None,
        'group': None,
    }

    return context


def get_staff_channel(user):
    context = {
        'university': None,
        'faculty': None,
        'group': None,
    }

    return context
