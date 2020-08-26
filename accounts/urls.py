from django.urls import path

from accounts.views.users import ListUsers

app_name = "accounts"
urlpatterns = [
    path("user/", ListUsers.as_view(), name='users-list'),
]
