from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
# Create your models here.
from users.managers import CustomUserManager


class CustomUser(AbstractUser):
    username = models.CharField(
        _('username'),
        max_length=150,
        blank=True,
        unique=True,
    )
    email = models.EmailField(_('email address'), unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
