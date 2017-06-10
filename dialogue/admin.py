from django.contrib import admin
from .models import *


class MessageModelAdmin(admin.ModelAdmin):
    list_display = ['dialogue', 'date', ]
    search_fields = ['dialogue', ]
    fields = ['dialogue', 'sender', 'text', ]
    readonly_fields = ['date', ]

    class Meta:
        model = Message


class DialogueModelAdmin(admin.ModelAdmin):
    list_display = ['pk', 'fresh_message_date', ]
    search_fields = []
    readonly_fields = ['fresh_message_date',]

    class Meta:
        model = Dialogue


admin.site.register(Message, MessageModelAdmin)
admin.site.register(Dialogue, DialogueModelAdmin)
