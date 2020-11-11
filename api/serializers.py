from rest_framework import serializers
from django.contrib.auth.models import User
from api.models import Course, Lesson, UserProfile


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
   class Meta:
        model = User
        fields = ("email", "id", "username", "is_superuser", "password")


# class ChangePasswordSerializer(serializers.Serializer):
#     model = User
#
#     old_password = serializers.CharField(required=True)
#     new_password = serializers.CharField(required=True)


class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

    redirect_url = serializers.CharField(max_length=500, required=False)

    class Meta:
        fields = ['email']
