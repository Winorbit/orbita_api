from django.urls import path, re_path
from django.contrib import admin
from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework.documentation import include_docs_urls
from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from api import users, courses
from rest_framework.routers import DefaultRouter

schema_view = get_schema_view(
   openapi.Info(
      title="Winorbit API",
      default_version='v1',
      description="",
      terms_of_service="",
      contact=openapi.Contact(email=""),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

router = DefaultRouter()
router.register(r'users', users.UserList, basename='users')
router.register(r'lessons', courses.LessonsList, basename='lessons')
router.register(r'groups', courses.GroupsList, basename='groups')
router.register(r'articles', courses.ArticlesList, basename='articles')
router.register(r'users_profiles', users.UserProfileClass)

urlpatterns = [re_path(r'^', include(router.urls)),
               re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
               re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
               re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

               re_path(r'^admin/', admin.site.urls),
               path('tinymce/', include('tinymce.urls')),
               path('search_user_by_email', users.search_user_by_email),
               path('add_user_to_group', users.add_user_to_group),
               path('search_userprofile', users.search_userprofile),
               path('update_user_info/<user_id>', users.update_user_info),

               re_path(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
            ]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
