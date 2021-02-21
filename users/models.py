from content.models import Course
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
# Create your models here.
from users.managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        _('username'),
        max_length=150,
        blank=True,
        null=True,
        default=""
    )
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    degree = models.ManyToManyField("content.Degree")
    pic = models.ImageField(default='default.png', upload_to='profile_pics')
    purchased_notes = models.ManyToManyField("content.Note")
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def get_courses(self):
        degree_id = self.degree.all().values_list('id')
        return Course.objects.filter(degree__in=degree_id)

    def get_full_name(self):
        return self.username

    def is_owner(self, resource):
        return resource.owner == self

    def has_purchased_note(self, note):
        return self.purchased_notes.filter(id=note.id).count() > 0
