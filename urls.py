from django.urls import path, re_path
from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.documentation import include_docs_urls
from rest_framework.schemas import get_schema_view

from api import users, courses

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'lessons', courses.LessonsList, basename='lessons')
router.register(r'courses', courses.CoursesList)
router.register(r'users', users.UserList, basename='users')
router.register(r'users_profiles', users.UserProfileClass)
#router.register(r'update_user_info', users.update_user_info)


urlpatterns = [re_path(r'^', include(router.urls)),
               path('search_userprofile', users.search_userprofile),
               path('search_user_by_email', users.search_user_by_email),
               path('request_restore_access', users.send_restore_access_email),
               path('reset_user_password', users.reset_user_password),
               path('lessons_course/<course_id>/', courses.lessons_course),

               re_path(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

               path('docs/', include_docs_urls(title='WinterOrbit')),

               path('schema/', get_schema_view(
                      title="WinterOrbit Service",
                      description="API for WinterOrbit"
                  ), name='openapi-schema'),
   re_path(r'^', include(router.urls)),
   path('search_userprofile', users.search_userprofile),
   path('search_user_by_email', users.search_user_by_email),
   path('update_user_info/<user_id>', users.update_user_info),
   path('lessons_course/<course_id>/', courses.lessons_course),
   path('send_email', users.send_email_for_orbita),

   re_path(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
