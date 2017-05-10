from django.shortcuts import render


def posts_list(request):
    return render(request, 'post/base.html')


def new_post(request):
    return render(request, 'post/base.html')
