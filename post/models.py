from django.db import models


class Post(models.Model):
    text = models.TextField(null=False)
    author = models.CharField(max_length=20, null=False)
    date = models.DateTimeField(null=False, auto_now=True)
    expires = models.DateTimeField(null=True)
    topic = models.CharField(max_length=20, null=True)
    # subject = models.ForeignKey(, null=True)


class Comment(models.Model):
    post = models.ForeignKey(Post, null=False, on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=20)
    text = models.CharField(max_length=200)
    date = models.DateTimeField(null=False, auto_now=True)
