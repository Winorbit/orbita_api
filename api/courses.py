from api.models import Article, Lesson, Group
from api.serializers import LessonSerializer, GroupSerializer, ArticleSerializer

from rest_framework import viewsets

class LessonsList(viewsets.ModelViewSet):
    queryset = Lesson.objects.all().order_by('-id')
    serializer_class = LessonSerializer 

class GroupsList(viewsets.ModelViewSet):
    queryset = Group.objects.all().order_by('-id')
    serializer_class = GroupSerializer 

class ArticlesList(viewsets.ModelViewSet):
    queryset = Article.objects.all().order_by('-id')
    serializer_class = ArticleSerializer 
