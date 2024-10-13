from django.urls import include, path
from rest_framework import routers, permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from .views import APIToken, DeleteAPIToken, SkillViewSet, TeamViewSet, DevelopmentViewSet, EmployViewSet, EmployeeSkillsViewSet, UpdateUserPassword


app_name = 'api'
v1_router = routers.DefaultRouter()
v1_router.register('development-plans', DevelopmentViewSet, basename='development-plans')
v1_router.register('employee-skills', EmployeeSkillsViewSet, basename='employeeskills')
v1_router.register('teams', TeamViewSet, basename='teams')
v1_router.register('skills', SkillViewSet, basename='skills')
v1_router.register('employees', EmployViewSet, basename='employees')


urlpatterns = [
    path('login/', APIToken.as_view(), name='token_create'),
    path('logout/', DeleteAPIToken.as_view(), name='token_delete'),
    path(
        'users/set_password/',
        UpdateUserPassword.as_view(),
        name='update_password'
    ),
    path('v1/', include(v1_router.urls)),
]


schema_view = get_schema_view(
   openapi.Info(
      title="Cats API",
      default_version='v1',
      description="Документация для приложения cats проекта Kittygram",
      contact=openapi.Contact(email="admin@kittygram.ru"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

# urlpatterns += [
#    url(r'^swagger(?P<format>\.json|\.yaml)$', 
#        schema_view.without_ui(cache_timeout=0), name='schema-json'),
#    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0),
#        name='schema-swagger-ui'),
#    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0),
#        name='schema-redoc'),
# ]
