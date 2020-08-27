from django.urls import path

from accounts.views.users import ListUser, UserDetail, MemberDetail

app_name = "accounts"

urlpatterns = [
    path("user", ListUser.as_view(), name="users-list"),
    path("user/<int:pk>", UserDetail.as_view(), name="user-detail"),
    path("member/<int:pk>", MemberDetail.as_view(), name="member-detail")
]
