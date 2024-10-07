from django.urls import path

from .views import APIToken, DeleteAPIToken

urlpatterns = [
    path('login/', APIToken.as_view(), name='token_create'),
    path('logout/', DeleteAPIToken.as_view(), name='token_delete')
]
