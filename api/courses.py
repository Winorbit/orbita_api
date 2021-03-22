from api.models import VideoLesson
from api.serializers import VideoLessonSerializer

from rest_framework import viewsets

class VideoLessonsList(viewsets.ModelViewSet):
    queryset = VideoLesson.objects.all().order_by('-id')
    serializer_class = VideoLessonSerializer
