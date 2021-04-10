from django.urls import path

from accounts.views.login import LoginView, LogoutView
from accounts.views.password import (ResetPasswordConfirm,
                                     ResetPasswordRequestCode, UpdatePassword)
from accounts.views.users import (AddMemberBranch, AddMemberRole, ListFollower,
                                  ListMember, ListMemberBranch, ListMemberRole,
                                  ListProfile, MemberBranchDetail,
                                  MemberDetail, MemberRoleDetail,
                                  ProfileDetail, ToggleMemberApprovalView,
                                  UserDetail, RegisterFollower)

app_name = "accounts"

urlpatterns = [
    path("register-follower", RegisterFollower.as_view(), name="register-follower"),
    path("user", ListFollower.as_view(), name="users-list"),
    path("member", ListMember.as_view(), name="members-list"),
    path("user/<int:pk>", UserDetail.as_view(), name="user-detail"),
    path("member/<int:pk>", MemberDetail.as_view(), name="member-detail"),
    path("member/<int:pk>/role", ListMemberRole.as_view(), name="member-list-role"),
    path("role", AddMemberRole.as_view(), name="member-create-role"),
    path("role/<int:pk>", MemberRoleDetail.as_view(), name="member-detail-role"),
    path("member/<int:pk>/branch", ListMemberBranch.as_view(), name="member-list-role"),
    path("member-branch", AddMemberBranch.as_view(), name="member-create-role"),
    path("member-branch/<int:pk>", MemberBranchDetail.as_view(), name="member-detail-role"),
    path("user/<int:pk>/profile", ListProfile.as_view(), name="profile-list"),
    path("profile/<int:pk>", ProfileDetail.as_view(), name="profile-detail"),
    path("login", LoginView.as_view(), name="s_login"),
    path("logout", LogoutView.as_view(), name="s_logout"),
    path("user/update-password", UpdatePassword.as_view(), name="update-password"),
    path("user/reset-password", ResetPasswordRequestCode.as_view(), name="reset-password-request"),
    path("user/reset-password/<str:code>/", ResetPasswordConfirm.as_view(), name="reset-password-confirm"),
    path("member/<int:pk>/toggle-approval", ToggleMemberApprovalView.as_view(), name="member-approval-toggle")
]
