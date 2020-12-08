import uuid
from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

class BaseTextModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=250, blank=False, default="hh")
    description = models.CharField(max_length=2500, default='f', blank=True)
    content = models.TextField(blank=False, default='f')
    
    def __str__(self):
        return self.title

class Course(BaseTextModel):
    pass


class Lesson(BaseTextModel):
    cours = models.ForeignKey(Course, related_name='course_for_lesson', on_delete=models.CASCADE)
    pass


class UserProfile(models.Model):
    profile_image = models.ImageField(upload_to="user_pics", blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_courses = ArrayField(models.CharField(max_length=36), blank=True)
