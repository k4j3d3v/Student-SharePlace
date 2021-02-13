import os

from django.db import models
from django.utils import timezone
from tinymce import models as tinymce_models


class Resource(models.Model):
    title = models.CharField(max_length=150)
    publ_date = models.DateTimeField(default=timezone.now)
    owner = models.ForeignKey("users.CustomUser", on_delete=models.CASCADE)

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
    uploaded = models.FileField(upload_to='resources/')


class Experience(Resource):
    kind_of = models.CharField(max_length=50)
    # text = models.CharField(max_length=1000)
    text = tinymce_models.HTMLField()
    course = models.ManyToManyField(Course)  # , related_name="related_to")
    degree = models.ForeignKey(Degree, on_delete=models.CASCADE, null=True, blank=True)
    uploaded = models.FileField(upload_to='resources/', null=True, blank=True)


class ExchangeRequest(models.Model):
    user_requester = models.ForeignKey("users.CustomUser", on_delete=models.CASCADE, related_name="requester")
    user_receiver = models.ForeignKey("users.CustomUser", on_delete=models.CASCADE, related_name="receiver")
    proposed_note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name="proposed")
    requested_note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name="requested")
    accepted = models.BooleanField(default=False)
    seen = models.BooleanField(default=False)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user_requester.username} wants exchange his <{self.proposed_note}> note with {self.user_receiver} " \
               f"notes about <{self.requested_note}>"

    class Meta:
        unique_together = ('proposed_note', 'requested_note')


class Notification(models.Model):
    user_receiver = models.ForeignKey("users.CustomUser", on_delete=models.CASCADE)
    request = models.ForeignKey(ExchangeRequest, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        action = "accepted" if self.request.accepted else "rejected"
        return f"{self.request.user_receiver} has {action} your exchange proposal."
