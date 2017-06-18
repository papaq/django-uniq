from datetime import datetime

from django.db import models
from customauth.models import UniqUser


class Dialogue(models.Model):
    participants = models.ManyToManyField(UniqUser)
    fresh_message_date = models.DateTimeField(auto_now_add=True, verbose_name='Time of newest message')

    def __str__(self):
        return 'Dialogue %s' % self.pk


class Message(models.Model):
    dialogue = models.ForeignKey(Dialogue, related_name='dialogues', on_delete=models.CASCADE, null=False, blank=False)
    sender = models.ForeignKey(UniqUser, related_name='dialogues', on_delete=models.CASCADE, null=False, blank=False)
    text = models.CharField(max_length=1000, blank=False, null=False)
    date = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        try:
            dialogue = Dialogue.objects.get(pk=self.dialogue.pk)
        except ValueError:
            return

        dialogue.fresh_message_date = datetime.now()
        dialogue.save()
        super(Message, self).save(*args, **kwargs)

    def __str__(self):
        return 'Message by %s on %s' % (self.sender, self.date)
