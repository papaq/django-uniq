from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, reverse

from channels.models import Group
from customauth.admin import UserCreationForm, UserChangeForm
from customauth.forms import UserLoginForm, UserProfileForm


def login_user(request):
    if request.user.is_authenticated():
        return redirect(reverse("channels:index"))

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


@login_required
def logout_user(request):
    logout(request)
    return redirect(reverse('customauth:login'))


def register_user(request):
    if request.user.is_authenticated():
        return redirect(reverse("channels:index"))

    form = UserCreationForm(request.POST or None)

    if form.is_valid():
        user = form.save(commit=False)

        # cleaned (normalized) data
        email = form.cleaned_data['email']
        password = form.cleaned_data["password1"]

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
    form = UserProfileForm(request.POST or None, request.FILES or None)

    if form.is_valid():

        new_first_name = form.clean_first_name()
        new_last_name = form.clean_last_name()
        new_avatar = form.cleaned_data['avatar']
        if (request.user.first_name != new_first_name
            or request.user.last_name != new_last_name
                or new_avatar is not None):

            request.user.first_name = new_first_name
            request.user.last_name = new_last_name
            if new_avatar is not None:
                request.user.avatar = new_avatar

            request.user.save()
            return redirect(reverse('customauth:profile'))

    user_kinds = {
        'T': 'Student',
        'C': 'Academic',
        'F': 'Staff',
    }

    context = {
        'form': form,
        'user_kind': user_kinds[request.user.user_kind],
    }

    return render(request, 'customauth/profile.html', context)


@login_required
def avatar_delete(request, pk):
    if pk == request.user.pk.__str__():
        request.user.avatar.delete(save=True)
        print(request.user.avatar)
    return redirect(reverse("customauth:profile"))


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
