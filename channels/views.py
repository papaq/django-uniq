import itertools
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse

from channels.models import University


@login_required
def channels_list(request):
    return render(request, "channels/channels_list.html")


@login_required
def initial(request):
    if request.user.is_authenticated():
        return redirect(reverse("channels:index"))


"""
def university_search_helper(count, query):
    model_list = University.objects.filter(title__icontains=query)
    return model_list[:count]
"""


def university_search_helper(count, query):
    model_list = University.objects.filter(title__icontains=query)
    words = query.split(' ')

    for L in range(1, count + 1):
        for subset in itertools.permutations(words, L):
            count1 = 1
            query1 = subset[0]
            while count1 != len(subset):
                query1 = query1 + " " + subset[count1]
                count1 += 1
            model_list = University.objects.filter(title__icontains=query1)
    return model_list.distinct()
