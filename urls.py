from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view
from django.urls import path, re_path
from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static

from api import users, courses

from rest_framework.routers import DefaultRouter
from rest_framework import permissions


router = DefaultRouter()
router.register(r'lessons', courses.LessonsList)
router.register(r'courses', courses.CoursesList)
router.register(r'users', users.UserList, basename='users')
router.register(r'users_profiles', users.UserProfileClass)

urlpatterns = [
   re_path(r'^', include(router.urls)),
   path('search_userprofile', users.search_userprofile),
   path('search_user_by_email', users.search_user_by_email),

   re_path(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    path('openapi/', get_schema_view(
        title="WinterOrbit Service",
        description="API developers hpoing to use our service"
    ), name='openapi-schema'),

    path('docs/', TemplateView.as_view(
        template_name='documentation.html',
        extra_context={'schema_url':'openapi-schema'}
    ), name='swagger-ui'),

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
