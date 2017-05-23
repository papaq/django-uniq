from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser,
    PermissionsMixin)
from django.db import models
from random import randrange

from channels.models import Group, Faculty, University


class MyUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Users must specify an email address')

        user = self.model(
            email=self.normalize_email(email),
            **extra_fields
        )

        user.first_name = user.first_name.title()
        user.last_name = user.last_name.title()

        if not user.media_dir:
            user.media_dir = "user%s" % (randrange(11121111, 99989999))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a User with the given email, 
        first and last names, kind and password.
        """
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given email,
        first and last names and password.
        """
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_admin', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        if extra_fields.get('is_admin') is not True:
            raise ValueError('Superuser must have is_admin=True.')

        return self._create_user(email, password, **extra_fields)


def upload_location(user, filename):
    lst = filename.split(".")
    extension = lst[-1]
    avatar_name = "avatar%s" % (randrange(111211, 999899))

    return "users/%s/%s.%s" % (user.media_dir, avatar_name, extension)


class UniqUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )

    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)

    USER_KINDS = (
        ('T', 'Student'),
        ('C', 'Academic'),
        ('F', 'Staff'),
    )

    user_kind = models.CharField(
        max_length=1,
        choices=USER_KINDS,
        default=USER_KINDS[0][0],
        blank=False)

    date_joined = models.DateTimeField(auto_now_add=True, auto_now=False)

    avatar = models.ImageField(
        upload_to=upload_location,
        width_field="width_field",
        height_field="height_field",
        null=True,
        blank=True,)

    width_field = models.IntegerField(default=128, null=True, blank=True)
    height_field = models.IntegerField(default=128, null=True, blank=True)

    media_dir = models.CharField(max_length=50, null=False, blank=False)

    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name='subscribers',
        null=True, blank=True)

    faculty = models.ForeignKey(
        Faculty,
        on_delete=models.CASCADE,
        related_name='subscribers',
        null=True, blank=True)

    university = models.ForeignKey(
        University,
        on_delete=models.CASCADE,
        related_name='subscribers',
        null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    # that one unique field, which is used at authentication
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    # by default
    # EMAIL_FIELD = 'email'

    def get_full_name(self):
        # The user is identified by their first and last names
        return "%s %s" % (self.first_name, self.last_name)

    def get_short_name(self):
        # The user is identified by their first name
        return self.first_name

    def __str__(self):              # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        """
        Does the user have a specific permission?
        Simplest possible answer: Yes, always
        """
        return True

    def has_module_perms(self, app_label):
        """
        Does the user have permissions to view the app `app_label`?
        Simplest possible answer: Yes, always
        """
        return True

    @property
    def is_staff(self):
        """
        Is the user a member of staff?
        Simplest possible answer: All admins are staff
        """
        return self.is_admin
