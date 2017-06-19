from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from random import randrange

from .models import UniqUser


class UserCreationForm(forms.ModelForm):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    """
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = UniqUser
        fields = ('email', 'first_name', 'last_name', 'user_kind', 'avatar')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])

        user.first_name = user.first_name.title()
        user.last_name = user.last_name.title()

        if not user.media_dir:
            user.media_dir = "users/user%s" % (randrange(11121111, 99989999))

        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = UniqUser
        fields = ('email', 'password', 'first_name', 'last_name', 'user_kind', 'avatar',)

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]

    def save(self, commit=True):
        user = super(UserChangeForm, self).save(commit=False)
        # user.set_password(self.cleaned_data["password"])

        user.first_name = user.first_name.title()
        user.last_name = user.last_name.title()

        if not user.media_dir:
            user.media_dir = "users/user%s" % (randrange(11121111, 99989999))

        if commit:
            user.save()
        return user


class UserAdmin(BaseUserAdmin):

    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'first_name', 'last_name', 'user_kind', 'is_admin')
    list_filter = ('is_admin', 'user_kind')
    fieldsets = (
        (None, {'fields': ('email', 'password',)}),
        ('Avatar', {'fields': ('avatar', 'width_field', 'height_field',)}),
        ('Personal info', {'fields': ('first_name', 'last_name',)}),
        ('Status', {'fields': ('user_kind',)}),
        ('Subscriptions', {'fields': ('university', 'faculty', 'group',)}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'user_kind', 'password1', 'password2')}
         ),
    )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    filter_horizontal = ()


# Now register the new UserAdmin...
admin.site.register(UniqUser, UserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)
