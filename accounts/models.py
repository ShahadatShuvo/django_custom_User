from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.safestring import mark_safe

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), blank=True)
    phone = models.CharField(
        _('Mobile Phone'), max_length=12, unique=True,
        validators=[RegexValidator(r'^[\d]{10,12}$',
                                   message='Format (ex: 01234567890)'
                                   )])
    first_name = models.CharField(
        _('First Name'), max_length=255, blank=True, null=True
    )

    last_name = models.CharField(
        _('Last Name'), max_length=255, blank=True, null=True
    )
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def __str__(self):
        return self.phone


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, unique=True
    )
    image = models.ImageField(upload_to='media/profile', default='no_pic.jpg', blank=True)

    bio = models.TextField(
        _('Bio'), blank=True, null=True
    )
    birth_date = models.DateField(
        _('Date of Birth'), blank=True, null=True
    )
    gender = models.CharField(
        _('Gender'), max_length=1, blank=True, null=True,
        choices=[('M', 'Male'), ('F', 'Female')]
    )

    is_active = models.BooleanField(
        _('Active'), default=True, null=True
    )
    created_at = models.DateTimeField(
        _('Created At'), auto_now_add=True, null=True
    )
    last_updated = models.DateTimeField(
        _('Last Updated'), auto_now=True, null=True
    )

    def __str__(self):
        return "Email: " + self.user.phone + ",   First Name: " + self.user.first_name

    @receiver(post_save, sender=User)
    def create_or_update_profile(sender, instance, created, **kwargs):
        """Creates or updates profile, when User object changes"""
        if created:
            Profile.objects.get_or_create(user=instance)
        instance.profile.save()

    def admin_photo(self):
        return mark_safe('<img src="{}" width="100" />'.format(self.image.url))

    admin_photo.short_description = 'Image'
    admin_photo.allow_tags = True


