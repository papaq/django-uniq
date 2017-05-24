from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, reverse

from channels.views import university_search_helper
from customauth.admin import UserCreationForm
from customauth.forms import UserLoginForm, UserProfileForm, UserSubscriptionForm, UserChooseForm


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

    university = request.user.university
    faculty = request.user.faculty
    group = request.user.group
    user_kind = user_kinds[request.user.user_kind]

    if user_kind is 'Student':
        place = 'group'
    else:
        place = 'department'

    warning = []
    if not university:
        warning += ['%s%s%s' % ('In order to receive and post news, subscribe to your ', place, ' please!')]

    success = []

    context = {
        'form': form,

        'user_info': {
            'user_kind': user_kind,
            'activity_place': place,

            'channels': [
                {
                    'name': 'university',
                    'content': university,
                },

                {
                    'name': 'faculty',
                    'content': faculty,
                },

                {
                    'name': 'group',
                    'content': group,
                },
            ]
        },

        'warning': warning,
        'success': success,
    }

    return render(request, 'customauth/profile.html', context)


@login_required
def avatar_delete(request, pk):
    if pk == request.user.pk.__str__():
        request.user.avatar.delete(save=True)
        print(request.user.avatar)
    return redirect(reverse("customauth:profile"))


@login_required
def unsubscription(request, channel):
    if channel == 'university':
        return redirect(reverse('customauth:unsubscribe_university', args=[request.user.pk]))

    if channel == 'faculty':
        return redirect(reverse('customauth:unsubscribe_faculty', args=[request.user.pk]))

    if channel == 'group':
        return redirect(reverse('customauth:unsubscribe_group', args=[request.user.pk]))

    return redirect(reverse('customauth:profile'))


@login_required
def unsubscribe_university(request, pk):
    if pk == request.user.pk.__str__():

        request.user.university = None
        request.user.faculty = None
        request.user.group = None
        request.user.save()
    return redirect(reverse("customauth:profile"))


@login_required
def unsubscribe_faculty(request, pk):
    if pk == request.user.pk.__str__():
        request.user.faculty = None
        request.user.group = None
        request.user.save()
    return redirect(reverse("customauth:profile"))


@login_required
def unsubscribe_group(request, pk):
    if pk == request.user.pk.__str__():
        request.user.group = None
        request.user.save()
    return redirect(reverse("customauth:profile"))


@login_required
def subscription(request, channel):
    if channel == 'university':
        return redirect(reverse('customauth:subscribe_university'))

    if channel == 'faculty':
        return redirect(reverse('customauth:subscribe_faculty'))

    if channel == 'group':
        return redirect(reverse('customauth:subscribe_group'))

    return redirect(reverse('customauth:profile'))


@login_required
def subscribe_university(request):
    form_search = UserSubscriptionForm(request.POST or None)
    form_choose = UserChooseForm(request.POST or None)

    results = []

    print('form is valid ???%s' % form_search.is_valid())
    if form_search.is_valid():
        search_request = form_search.cleaned_data['search_request']
        results = university_search_helper(4, search_request)
        choice = {'choice': (('a', 'a'),)}
        form_choose.__init__(kwargs=choice)
        print(results)

    warning = []

    context = {
        'form_search': form_search,
        'form_choose': form_choose,
        'channel': 'university',
        'attention': warning,
        'results': results,
    }

    return render(request, 'customauth/subscription.html', context)


@login_required
def subscribe_faculty(request):
    if request.user.university is None:
        return redirect(reverse('customauth:subscribe_university'))

    form_search = UserSubscriptionForm(request.POST or None)
    form_choose = UserChooseForm(request.POST or None)

    results = []

    print('form is valid ???' + form_search.is_valid())
    if form_search.is_valid():
        search_request = form_search.cleaned_data['search_request']
        results = university_search_helper(4, search_request)

        if request.user.university is None:
            return redirect(reverse('customauth:subscribe_university'))

        # save changes

    warning = []

    context = {
        'form_search': form_search,
        'form_choose': form_choose,
        'channel': 'faculty',
        'attention': warning,
        'results': results,
    }

    return render(request, 'customauth/subscription.html', context)


@login_required
def subscribe_group(request):
    if request.user.user_kind is not 'T':
        return redirect(reverse('customauth:profile'))
    if request.user.faculty is None:
        return redirect(reverse('customauth:subscribe_faculty'))

    form_search = UserSubscriptionForm(request.POST or None)
    form_choose = UserChooseForm(request.POST or None)

    results = []

    if form_search.is_valid():
        search_request = form_search.cleaned_data['search_request']
        results = university_search_helper(4, search_request)
        print(results)

        if request.user.faculty is None:
            return redirect(reverse('customauth:subscribe_faculty'))

        # save changes

    warning = []

    context = {
        'form_search': form_search,
        'form_choose': form_choose,
        'channel': 'group',
        'attention': warning,
        'results': results,
    }

    return render(request, 'customauth/subscription.html', context)
