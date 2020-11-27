from django.urls import path

from accounts.views.login import LoginView, LogoutView
from accounts.views.password import (ResetPasswordConfirm,
                                     ResetPasswordRequestCode, UpdatePassword)
from accounts.views.users import (ListFollower, ListMember, MemberDetail,
                                  ToggleMemberApprovalView, UserDetail)

app_name = "accounts"

urlpatterns = [
    path("user", ListFollower.as_view(), name="users-list"),
    path("member", ListMember.as_view(), name="members-list"),
    path("user/<int:pk>", UserDetail.as_view(), name="user-detail"),
    path("member/<int:pk>", MemberDetail.as_view(), name="member-detail"),
    path("login", LoginView.as_view(), name="s_login"),
    path("logout", LogoutView.as_view(), name="s_logout"),
    path("user/update-password", UpdatePassword.as_view(), name="update-password"),
    path("user/reset-password", ResetPasswordRequestCode.as_view(), name="reset-password-request"),
    path("user/reset-password/<str:code>/", ResetPasswordConfirm.as_view(), name="reset-password-confirm"),
    path("member/<int:pk>/toggle-approval", ToggleMemberApprovalView.as_view(), name="member-approval-toggle")
]
