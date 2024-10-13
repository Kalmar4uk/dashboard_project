from django.urls import include, path
from rest_framework import routers

from .views import APIToken, DeleteAPIToken, UserViewSet, SkillViewSet, TeamViewSet, DevelopmentViewSet, EmployViewSet, EmployeeSkillsViewSet


app_name = 'api'
v1_router = routers.DefaultRouter()
v1_router.register('development-plans', DevelopmentViewSet, basename='development-plans')
v1_router.register('employee-skills', EmployeeSkillsViewSet, basename='employeeskills')
v1_router.register('teams', TeamViewSet, basename='teams')
v1_router.register('skills', SkillViewSet, basename='skills')
v1_router.register('employees', EmployViewSet, basename='employees')
v1_router.register('users', UserViewSet, basename='users')


urlpatterns = [
    path('login/', APIToken.as_view(), name='token_create'),
    path('logout/', DeleteAPIToken.as_view(), name='token_delete'),
    path('v1/', include(v1_router.urls)),
]
