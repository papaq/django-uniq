from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse

from channels.utils import combine_sets, count_new_messages
from post.models import Post


@login_required
def stream(request):
    user = request.user

    context = {
        'active': 'stream',
        'new_posts': 0,
        'channels': {
            'university_channel': {
                'item': None,
                'new_posts': None
            },
            'faculty_channel': {
                'item': None,
                'new_posts': None
            },
            'group_set_channel': {
                'item': None,
                'new_posts': None
            },
            'group_channel': {
                'item': None,
                'new_posts': None
            },
        },
        'subgroup_channels': None,
        'posts': None,
    }
    template = "channels/channels_stream.html"

    if not user.university:
        return render(request, "channels/channels_stream.html", context)

    university_posts = Post.objects.filter(university=user.university).exclude(done=user).order_by('date')
    context['channels']['university_channel']['item'] = user.university
    university_posts_new = count_new_messages(university_posts, user)
    context['channels']['university_channel']['new_posts'] = university_posts_new

    if not user.faculty:
        context['posts'] = university_posts
        context['new_posts'] = university_posts_new

        return render(request, template, context)

    faculty_posts = Post.objects.filter(faculty=user.faculty).exclude(done=user).order_by('date')
    context['channels']['faculty_channel']['item'] = user.faculty
    faculty_posts_new = count_new_messages(faculty_posts, user)
    context['channels']['faculty_channel']['new_posts'] = faculty_posts_new

    group_set_posts = None
    group_posts = None
    subgroups_posts = None
    subjects_posts = None

    group_set_posts_new = 0
    group_posts_new = 0

    if user.group:
        group_set_posts = Post.objects.filter(group_set__groups=user.group).exclude(done=user).order_by('date')
        context['channels']['group_set_channel']['item'] = user.group.group_set
        group_set_posts_new = count_new_messages(group_set_posts, user)
        context['channels']['group_set_channel']['new_posts'] = group_set_posts_new

        group_posts = Post.objects.filter(group=user.group).exclude(done=user).order_by('date')
        context['channels']['group_channel']['item'] = user.group
        group_posts_new = count_new_messages(group_posts, user)
        context['channels']['group_channel']['new_posts'] = group_posts_new

        # Find all subgroups
        # Find all posts in those subgroups

        # Find all subject of group
        # Get posts from there

    if user.user_kind is not 'F':
        # Find all individual course subs
        # Get posts from there
        pass

    posts = combine_sets(
        university_posts=university_posts,
        faculty_posts=faculty_posts,
        group_set_posts=group_set_posts,
        group_posts=group_posts,
        subgroups_posts=subgroups_posts,
        subjects_posts=subjects_posts,
    )

    context['posts'] = posts.order_by('date')
    context['new_posts'] = university_posts_new + faculty_posts_new + group_set_posts_new + group_posts_new

    return render(request, template, context)


@login_required
def initial(request):
    if request.user.is_authenticated():
        return redirect(reverse("channels:index"))
