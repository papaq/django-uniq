from django.shortcuts import redirect
from django.urls import reverse


def redirect_back(request):
    return redirect(reverse('channels:index'))