from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, reverse

from channels import search_helper
from channels.models import University, Faculty, Group
from customauth.admin import UserCreationForm
from customauth.forms import UserLoginForm, UserProfileForm, UserSubscriptionForm, UserChoiceForm


def login_user(request):
    if request.user.is_authenticated():
        return redirect(reverse("channels:stream"))

    form = UserLoginForm(request.POST or None)

    if form.is_valid():
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = authenticate(request, email=email, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)

                if not hasattr(request, 'next'):
                    return redirect(reverse('channels:stream'))
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
        return redirect(reverse("channels:stream"))

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
                    return redirect(reverse('customauth:profile'))
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
    form_choose = None

    channel = 'university'
    results = []
    warnings = []
    previous_value = ''
    if request.user.university:
        previous_value = request.user.university.title

    if form_search.is_valid():
        search_request = form_search.cleaned_data['search_request']
        previous_value = search_request
        result_query = search_helper.university_search_helper(10, search_request)

        for university in result_query:
            results.insert(0, (university.pk, "%s (%s)" % (university.title, university.city)))

        if results:
            form_choose = UserChoiceForm(choices=results)
        else:
            warnings += ["We still don't serve your %s, call 911!" % channel]
            form_choose = None

    context = {
        'form_search': form_search,
        'form_choose': form_choose,
        'previous_value': previous_value,
        'channel': channel,
        'warnings': warnings,
    }

    return render(request, 'customauth/subscription.html', context)


@login_required
def subscribe_faculty(request):
    if request.user.university is None:
        return redirect(reverse('customauth:subscribe_university'))

    form_search = UserSubscriptionForm(request.POST or None)
    form_choose = None

    channel = 'faculty'
    warnings = []
    results = []
    previous_value = ''
    if request.user.faculty:
        previous_value = request.user.faculty.title

    if form_search.is_valid():
        search_request = form_search.cleaned_data['search_request']
        previous_value = search_request
        result_query = search_helper.faculty_search_helper(10, search_request, request.user.university.pk)

        for faculty in result_query:
            results.insert(0, (faculty.pk, faculty.title))

        if results:
            form_choose = UserChoiceForm(choices=results)
        else:
            warnings += ["We still don't serve your %s, call 911!" % channel]
            form_choose = None

    context = {
        'form_search': form_search,
        'form_choose': form_choose,
        'previous_value': previous_value,
        'channel': channel,
        'wornings': warnings,
    }

    return render(request, 'customauth/subscription.html', context)


@login_required
def subscribe_group(request):
    if request.user.user_kind is not 'T':
        return redirect(reverse('customauth:profile'))
    if request.user.faculty is None:
        return redirect(reverse('customauth:subscribe_faculty'))

    form_search = UserSubscriptionForm(request.POST or None)
    form_choose = None

    channel = 'group'
    results = []
    warnings = []
    previous_value = ''
    if request.user.group:
        previous_value = request.user.group.title

    if form_search.is_valid():
        search_request = form_search.cleaned_data['search_request']
        previous_value = search_request
        result_query = search_helper.group_search_helper(10, search_request, request.user.faculty.pk)

        for group in result_query:
            results.insert(0, (group.pk, "%s (%s)" % (group.title, group.group_set.show_title)))

        if results:
            form_choose = UserChoiceForm(choices=results)
        else:
            warnings += ["We still don't serve your %s, call 911!" % channel]
            form_choose = None

    context = {
        'form_search': form_search,
        'form_choose': form_choose,
        'previous_value': previous_value,
        'channel': channel,
        'warnings': warnings,
    }

    return render(request, 'customauth/subscription.html', context)


@login_required
def save_subscription(request, channel_level=None):
    channel_pk = int(request.POST.get('choice', ''))

    if not channel_level or not channel_pk:
        return redirect(reverse('customauth:profile'))

    if channel_level == 'university':
        request.user.faculty = request.user.group = None
        uni = University.objects_safe.safe_get(pk=channel_pk)
        if uni:
            request.user.university = uni
            request.user.save()

    elif channel_level == 'faculty':
        request.user.group = None
        uni = request.user.university

        # Check if university record exists
        if not uni:
            return redirect(reverse('customauth:profile'))

        faculty = Faculty.objects_safe.safe_get(pk=channel_pk)
        if faculty:
            request.user.faculty = faculty
            request.user.save()

    elif channel_level == 'group':
        # Check if university record exists
        if not request.user.university:
            return redirect(reverse('customauth:profile'))

        # Check if faculty record exists
        if not request.user.faculty:
            return redirect(reverse('customauth:profile'))

        group = Group.objects_safe.safe_get(pk=channel_pk)
        if group:
            request.user.group = group
            request.user.save()

    return redirect(reverse('customauth:profile'))
