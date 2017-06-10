from django.contrib import admin
from .models import *


class MessageModelAdmin(admin.ModelAdmin):
    list_display = ['dialogue', 'date', ]
    search_fields = ['dialogue', ]

    class Meta:
        model = Message


class DialogueModelAdmin(admin.ModelAdmin):
    list_display = ['pk', 'fresh_message_date', ]
    search_fields = []

    class Meta:
        model = Dialogue


admin.site.register(Message, MessageModelAdmin)
admin.site.register(Dialogue, DialogueModelAdmin)
