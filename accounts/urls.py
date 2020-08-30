from django.urls import path

from accounts.views.login import LoginView, LogoutView
from accounts.views.password import UpdatePassword, ResetPasswordRequestCode, ResetPasswordConfirm
from accounts.views.users import ListUser, UserDetail, MemberDetail

app_name = "accounts"

urlpatterns = [
    path("user", ListUser.as_view(), name="users-list"),
    path("user/<int:pk>", UserDetail.as_view(), name="user-detail"),
    path("member/<int:pk>", MemberDetail.as_view(), name="member-detail"),
    path("login", LoginView.as_view(), name="s_login"),
    path("logout", LogoutView.as_view(), name="s_logout"),
    path("user/update-password", UpdatePassword.as_view(), name="update-password"),
    path("user/reset-password", ResetPasswordRequestCode.as_view(), name="reset-password-request"),
    path("user/reset/password/<str:code>/", ResetPasswordConfirm.as_view(), name="reset-password-confirm")
]
