from django.shortcuts import render


def channels_list(request):
    return render(request, "channels/channels_list.html")
