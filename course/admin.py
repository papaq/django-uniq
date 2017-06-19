from django.contrib import admin

from course.models import Subject


class SubjectModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'channel', 'date_start', 'date_start']
    search_fields = ['title', 'channel',]
    fields = ['title', 'description', 'channel', 'date_start', 'date_finish', 'is_open', 'max_points', 'teachers', ]
    readonly_fields = ['media_dir', ]

    class Meta:
        model = Subject


admin.site.register(Subject, SubjectModelAdmin)
