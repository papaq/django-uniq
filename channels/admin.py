from django.contrib import admin

from .models import *


class UniversityModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'city', 'country']
    search_fields = ['title', 'city', 'country']

    class Meta:
        model = University


class FacultyModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'get_university_title']
    search_fields = ['title', ]

    class Meta:
        model = Faculty


class GroupStackModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'get_university_title', 'get_faculty_title', 'year_enter', 'year_graduate']
    search_fields = ['title', 'year_enter', 'year_graduate']

    class Meta:
        model = GroupStack


class GroupModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'get_university_title', 'get_faculty_title', 'get_group_stack_title']
    search_fields = ['title', ]

    class Meta:
        model = Group


admin.site.register(University, UniversityModelAdmin)
admin.site.register(Faculty, FacultyModelAdmin)
admin.site.register(GroupStack, GroupStackModelAdmin)
admin.site.register(Group, GroupModelAdmin)
