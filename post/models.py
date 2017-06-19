from django.db import models

from channels.models import University, Faculty, GroupSet, Group
from course.models import Subject
from customauth.models import UniqUser


class Post(models.Model):
    title = models.CharField(max_length=150, null=False)
    text = models.CharField(max_length=5000, null=False)
    author = models.ForeignKey(UniqUser, on_delete=models.CASCADE, related_name='posts', null=False)

    is_subject = models.BooleanField(default=False)
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='posts', null=True, blank=True)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='posts', null=True, blank=True)
    group_set = models.ForeignKey(GroupSet, on_delete=models.CASCADE, related_name='posts', null=True, blank=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='posts', null=True, blank=True)

    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='posts', null=True, blank=True)

    date = models.DateTimeField(auto_now_add=True, editable=False)
    expires = models.DateTimeField(null=True, blank=True)

    read = models.ManyToManyField(UniqUser, related_name='read_posts')
    starred = models.ManyToManyField(UniqUser, related_name='starred_posts')
    done = models.ManyToManyField(UniqUser, related_name='done_posts')

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, null=False, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(UniqUser, null=False, on_delete=models.CASCADE, related_name='comments')
    text = models.CharField(max_length=1000)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'Comment on "%s"' % self.post.title
