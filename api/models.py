from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from tinymce import models as tinymce_models

class Lesson(models.Model):
    title = models.CharField(max_length=250, blank=False, default="")
    source_link = models.CharField(max_length=2500, default='', blank=False)
    lesson_description = tinymce_models.HTMLField()
    lesson_usefull_links = tinymce_models.HTMLField()

    class Meta:
        managed = True
        db_table = 'Lessons'
        verbose_name_plural = "Lessons"

    def __str__(self):
        return self.title


class Group(models.Model):
    title = models.CharField(max_length=350, blank=False, default="")
    discord_chat_link = models.CharField(max_length=1000, default='', blank=False)

    class Meta:
        managed = True
        db_table = 'Groups'
        verbose_name_plural = "Groups"

    def __str__(self):
        return self.title


class VideoLesson(models.Model):
    title = models.CharField(max_length=250, blank=False, default="")
    description = models.CharField(max_length=2500, default='', blank=True)
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
    groups = ArrayField(models.CharField(max_length=10, blank=True), blank=True, default=list)

    def __str__(self):
        return self.user.username
