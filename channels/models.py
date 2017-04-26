from django.db import models
from django.utils import timezone

class Country(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class City(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='cities')
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class University(models.Model):
    title = models.CharField(max_length=200)
    info = models.TextField(blank=True, null=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='universities')

    def __str__(self):
        return self.title

class Faculty(models.Model):
    title = models.CharField(max_length=200)
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='faculties')

    def __str__(self):
        return self.title

class Department(models.Model):
    title = models.CharField(max_length=200)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='departments')

    def __str__(self):
        return self.title

class GroupStack(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='group_stacks')
    info =  models.TextField(blank=True, null=True)
    year_enter = models.DateTimeField(null=False)
    year_graduate = models.DateTimeField(null=False)

    def __str__(self):
        return self.department + ' group stack of ' + self.year_enter.year

class Group(models.Model):
    title = models.CharField(max_length=50)
    group_stack = models.ForeignKey(GroupStack, on_delete=models.CASCADE, related_name='groups')

    def __str__(self):
        return self.title

class Subscriptions(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='subscriptions')
    student = models.Integer(null=Falsw) # models.ForeignKey(User)
