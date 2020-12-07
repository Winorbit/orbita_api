from api.models import Course, Lesson
from api.serializers import CourseSerializer, LessonSerializer

from rest_framework.decorators import api_view
from django.shortcuts import get_list_or_404
from rest_framework.response import Response
from rest_framework import status, viewsets



class LessonsList(viewsets.ModelViewSet):
    queryset = Lesson.objects.all().order_by('-id')
    serializer_class = LessonSerializer

class CoursesList(viewsets.ModelViewSet):
    queryset = Course.objects.all().order_by('-id')
    serializer_class = CourseSerializer


class LessonsList(viewsets.ModelViewSet):
    queryset = Lesson.objects.all().order_by('-id')
    serializer_class = LessonSerializer


@api_view(['GET'])
def lessons_course(request, course_id=None):
    queryset = Lesson.objects.all()
    lessons = get_list_or_404(queryset, cours=course_id)
    serializer = LessonSerializer(lessons, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
