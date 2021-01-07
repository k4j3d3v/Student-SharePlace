import os

from django.db import models
from django.utils import timezone
from users.models import CustomUser


class Resource(models.Model):
    title = models.CharField(max_length=150)
    publ_date = models.DateTimeField(default=timezone.now)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    uploaded = models.FileField(upload_to='resources/', null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('content:%s-detail' % self.get_cname().lower(), args=[str(self.id)])

    def get_cname(self):
        return self.__class__.__name__

    def get_filename(self):
        return os.path.basename(self.uploaded.name)


class Degree(models.Model):
    name = models.CharField(max_length=150)
    BACHELOR = 'LT'
    MASTER = 'LM'
    DEGREE_TYPE_CHOICES = [
        (BACHELOR, 'Laurea Triennale'),
        (MASTER, 'Laurea Magistrale')
    ]
    type_of = models.CharField(
        max_length=2,
        choices=DEGREE_TYPE_CHOICES,
    )

    def __str__(self):
        return self.type_of + '-' + self.name


class Course(models.Model):
    name = models.CharField(max_length=150)
    credits = models.IntegerField()
    lecturer = models.CharField(max_length=150)
    degree = models.ManyToManyField(Degree)

    def __str__(self):
        return self.name


class Note(Resource):
    path = models.CharField(max_length=250)
    price = models.FloatField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)


class Experience(Resource):
    kind_of = models.CharField(max_length=50)
    text = models.TextField()
    course = models.ManyToManyField(Course)  # , related_name="related_to")
    degree = models.ManyToManyField(Degree, related_name="related_to", null=True, blank=True)
