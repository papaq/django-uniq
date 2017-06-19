from random import randrange

from django.db import models

from channels.models import CourseChannel
from customauth.models import UniqUser


class Subject(models.Model):
    title = models.CharField(max_length=200, null=False)
    description = models.TextField(null=False)

    channel = models.ForeignKey(CourseChannel, on_delete=models.CASCADE, null=False,
                                related_name='subjects')

    date_start = models.DateField(auto_now_add=False, null=False)
    date_finish = models.DateField(auto_now_add=False, null=False)

    is_open = models.BooleanField(default=False)

    max_points = models.IntegerField(default=100)
    teachers = models.ManyToManyField(UniqUser, related_name='courses_i_lead')

    media_dir = models.CharField(max_length=100, null=False, blank=False, default=None)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.media_dir:
            self.media_dir = "courses/course%s" % (randrange(11121111, 99989999))

        print(hasattr(self, 'channel'))
        if not self.channel:
            print('aaa')
            channel = CourseChannel(title=self.title)
            channel.save()
            self.channel = channel
        super(Subject, self).save(*args, **kwargs)
