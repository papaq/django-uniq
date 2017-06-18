from django.shortcuts import redirect
from django.urls import reverse


def redirect_to_stream(request):
    return redirect(reverse('channels:stream'))
