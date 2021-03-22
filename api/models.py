import uuid
from django.db import models
from django.contrib.auth.models import User

class VideoLesson(models.Model):
    title = models.CharField(max_length=250, blank=False, default="default")
    description = models.CharField(max_length=2500, default='default', blank=True)
    source_link = models.CharField(max_length=2500, default='', blank=False)

    class Meta:
        managed = True
        db_table = 'videolesson'
        verbose_name_plural = "videolesson"

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    profile_image = models.ImageField(upload_to="user_pics", blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
