from django.db import models


class University(models.Model):
    title = models.CharField(max_length=200)
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "universities"

    def __str__(self):
        return self.title


class Faculty(models.Model):
    title = models.CharField(max_length=200)
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name="faculties")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "faculties"


class GroupStack(models.Model):
    title = models.CharField(max_length=20)

    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name="groupstacks")
    info = models.TextField(blank=True, null=True)
    year_enter = models.DateTimeField(null=False)
    year_graduate = models.DateTimeField(null=False)

    def __str__(self):
        return self.title


class Group(models.Model):
    title = models.CharField(max_length=50)
    group_stack = models.ForeignKey(GroupStack, on_delete=models.CASCADE, related_name='groups')

    def __str__(self):
        return self.title
