import datetime
from django.db import models


class UniversityModelManager(models.Manager):
    def safe_get(self, pk):
        try:
            obj = University.objects.get(pk=pk)
        except University.DoesNotExist:
            obj = None
        return obj


class FacultyModelManager(models.Manager):
    def safe_get(self, pk):
        try:
            obj = Faculty.objects.get(pk=pk)
        except Faculty.DoesNotExist:
            obj = None
        return obj


class GroupStackModelManager(models.Manager):
    def safe_get(self, pk):
        try:
            obj = GroupStack.objects.get(pk=pk)
        except GroupStack.DoesNotExist:
            obj = None
        return obj


class GroupModelManager(models.Manager):
    def safe_get(self, pk):
        try:
            obj = Group.objects.get(pk=pk)
        except Group.DoesNotExist:
            obj = None
        return obj


def year_choices():
    years = []
    for r in range(2010, 2030):
        years.append((r, r))
    return years


class University(models.Model):
    title = models.CharField(max_length=200, unique=True)
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)

    objects = models.Manager()
    objects_safe = UniversityModelManager()  # safe search

    class Meta:
        verbose_name_plural = "universities"

    def __str__(self):
        return self.title


class Faculty(models.Model):
    title = models.CharField(max_length=200)
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name="faculties")

    objects = models.Manager()
    objects_safe = FacultyModelManager()  # safe search

    def __str__(self):
        return self.title

    def get_university_title(self):
        return self.university.title

    class Meta:
        verbose_name_plural = "faculties"


class GroupStack(models.Model):
    title = models.CharField(max_length=100)
    show_title = models.CharField(max_length=104, null=True, blank=True, editable=False)

    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name="groupstacks")
    info = models.TextField(blank=True, null=True)
    year_enter = models.IntegerField(choices=year_choices(), default=datetime.datetime.now().year, null=False)
    year_graduate = models.IntegerField(choices=year_choices(), default=datetime.datetime.now().year + 4, null=False)

    objects = models.Manager()
    objects_safe = GroupStackModelManager()  # safe search

    def __str__(self):
        return self.title

    def get_university_title(self):
        return self.faculty.university.title

    def get_faculty_title(self):
        return self.faculty.title

    def save(self, *args, **kwargs):
        self.show_title = "%s%s%d%s%d" % (self.title, ' ', self.year_enter, '-', self.year_graduate)
        super(GroupStack, self).save(*args, **kwargs)


class Group(models.Model):
    title = models.CharField(max_length=50)
    group_stack = models.ForeignKey(GroupStack, on_delete=models.CASCADE, related_name='groups')

    objects = models.Manager()
    objects_safe = GroupModelManager()  # safe search

    def __str__(self):
        return self.title

    def get_university_title(self):
        return self.group_stack.faculty.university.title

    def get_faculty_title(self):
        return self.group_stack.faculty.title

    def get_group_stack_title(self):
        return self.group_stack.title
