from django.shortcuts import render


def posts_list(request):
    return render(request, 'channels/base.html')


def new_post(request):
    return render(request, 'channels/base.html')
