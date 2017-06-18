from django.contrib import admin

from post.models import Post


class PostModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'date', 'is_subject']
    search_fields = ['title', 'author', 'university', 'faculty', 'group_set', 'group']
    fields = ['title', 'text', 'author', 'is_subject', 'university', 'faculty', 'group_set', 'group', 'subject', 'expires']
    readonly_fields = ['date', ]

    class Meta:
        model = Post


admin.site.register(Post, PostModelAdmin)
