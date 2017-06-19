from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from channels.utils import combine_sets, count_recent_posts
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

    university_posts = Post.objects.filter(university=user.university).exclude(done=user)
    context['channels']['university_channel']['item'] = user.university
    university_posts_new = count_recent_posts(university_posts, user)
    context['channels']['university_channel']['new_posts'] = university_posts_new

    if not user.faculty:
        context['posts'] = university_posts.order_by('date')
        context['new_posts'] = university_posts_new

        return render(request, template, context)

    faculty_posts = Post.objects.filter(faculty=user.faculty).exclude(done=user)
    context['channels']['faculty_channel']['item'] = user.faculty
    faculty_posts_new = count_recent_posts(faculty_posts, user)
    context['channels']['faculty_channel']['new_posts'] = faculty_posts_new

    group_set_posts = None
    group_posts = None
    subgroups_posts = None
    subjects_posts = None

    group_set_posts_new = 0
    group_posts_new = 0

    if user.group:
        group_set_posts = Post.objects.filter(group_set__groups=user.group).exclude(done=user)
        context['channels']['group_set_channel']['item'] = user.group.group_set
        group_set_posts_new = count_recent_posts(group_set_posts, user)
        context['channels']['group_set_channel']['new_posts'] = group_set_posts_new

        group_posts = Post.objects.filter(group=user.group).exclude(done=user)
        context['channels']['group_channel']['item'] = user.group
        group_posts_new = count_recent_posts(group_posts, user)
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


class SearchView(View, LoginRequiredMixin):
    def post(self, request, *args, **kwargs):
        search_string = request.POST.get('search')

        user = request.user
        template = 'channels/search.html'
        context = {
            'request': search_string,
            'count': 0,
            'sections': {
                'channel_posts': {
                    'posts': None,
                    'title': "Section: Channels' posts"
                },
                'subject_posts': {
                    'posts': None,
                    'title': "Section: Subjects' posts"
                },
            },
        }

        if not user.university:
            return render(request, "channels/search.html", context)

        university_posts = Post.objects.filter(university=user.university, title__icontains=search_string).exclude(done=user)

        if not user.faculty:
            if university_posts:
                university_posts = university_posts.order_by('date')

            context['sections']['channel_posts']['posts'] = university_posts

            if university_posts:
                context['count'] = len(university_posts)
            return render(request, template, context)

        faculty_posts = Post.objects.filter(faculty=user.faculty, title__icontains=search_string).exclude(done=user)

        group_set_posts = None
        group_posts = None
        subgroups_posts = None
        subjects_posts = None

        if user.group:
            group_set_posts = Post.objects.filter(group_set__groups=user.group, title__icontains=search_string).exclude(done=user)
            group_posts = Post.objects.filter(group=user.group, title__icontains=search_string).exclude(done=user)

            # Find all subgroups
            # Find all posts in those subgroups

            # Find all subject of group
            # Get posts from there

        if user.user_kind is not 'F':
            # Find all individual course subs
            # Get posts from there
            pass

        channel_posts = combine_sets(
            university_posts=university_posts,
            faculty_posts=faculty_posts,
            group_set_posts=group_set_posts,
            group_posts=group_posts,
            subgroups_posts=subgroups_posts,
        )

        if channel_posts:
            channel_posts.order_by('date')

        if subjects_posts:
            subjects_posts.order_by('date')

        context['sections']['channel_posts']['posts'] = channel_posts
        context['sections']['subject_posts']['posts'] = subjects_posts

        count_channel_posts = 0
        if channel_posts:
            count_channel_posts = len(channel_posts)

        count_subject_posts = 0
        if subjects_posts:
            count_subject_posts = len(subjects_posts)

        context['count'] = count_channel_posts + count_subject_posts


        return render(request, template, context)
