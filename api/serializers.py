from rest_framework import serializers
from django.contrib.auth.models import User
from api.models import  UserProfile, Lesson, Group, Article

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "id", "username", "is_superuser", "password", "is_staff")

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields =  "__all__"

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields =  "__all__"

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields =  "__all__"
