from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse


@login_required
def channels_list(request):
    return render(request, "channels/channels_list.html")


@login_required
def initial(request):
    if request.user.is_authenticated():
        return redirect(reverse("channels:index"))
