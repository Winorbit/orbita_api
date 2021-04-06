from api.models import VideoLesson, Lesson, Group
from api.serializers import VideoLessonSerializer, LessonSerializer, GroupSerializer

from rest_framework import viewsets

class VideoLessonsList(viewsets.ModelViewSet):
    queryset = VideoLesson.objects.all().order_by('-id')
    serializer_class = VideoLessonSerializer

class LessonsList(viewsets.ModelViewSet):
    queryset = Lesson.objects.all().order_by('-id')
    serializer_class = LessonSerializer 

class GroupsList(viewsets.ModelViewSet):
    queryset = Group.objects.all().order_by('-id')
    serializer_class = GroupSerializer 
