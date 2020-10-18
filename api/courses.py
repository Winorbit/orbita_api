from api.models import Course, Lesson
from api.serializers import CourseSerializer, LessonSerializer

from rest_framework import  viewsets

class LessonsList(viewsets.ModelViewSet):
    queryset = Lesson.objects.all().order_by('-id')
    serializer_class = LessonSerializer

class CoursesList(viewsets.ModelViewSet):
    queryset = Course.objects.all().order_by('-id')
    serializer_class = CourseSerializer
