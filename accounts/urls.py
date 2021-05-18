from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from rest_framework.routers import DefaultRouter

from accounts.views.login import LoginView, LogoutView
from accounts.views.member import ListMember, MemberDetail, ToggleMemberApprovalView
from accounts.views.member_branch import ListMemberBranch, AddMemberBranch, MemberBranchDetail
from accounts.views.member_role import ListMemberRole, CreateMemberRole, MemberRoleDetail
from accounts.views.password import (ResetPasswordConfirm,
                                     ResetPasswordRequestCode, UpdatePassword)
from accounts.views.profile import ProfileImageViewSet, UserProfile, ProfileDetail
from accounts.views.register_follower import RegisterFollower
from accounts.views.users import ListFollower, UserDetail

app_name = "accounts"

router = DefaultRouter()
router.register(r"profile-image", ProfileImageViewSet, basename="profile-image")
urlpatterns = router.urls

urlpatterns += [
    path("register-follower", RegisterFollower.as_view(), name="register-follower"),
    path("user", ListFollower.as_view(), name="users-list"),
    path("member", ListMember.as_view(), name="members-list"),
    path("user/<int:pk>", UserDetail.as_view(), name="user-detail"),
    path("member/<int:pk>", MemberDetail.as_view(), name="member-detail"),
    path("member/<int:pk>/role", ListMemberRole.as_view(), name="member-list-role"),
    path("role", CreateMemberRole.as_view(), name="member-create-role"),
    path("role/<int:pk>", MemberRoleDetail.as_view(), name="member-detail-role"),
    path("member/<int:pk>/branch", ListMemberBranch.as_view(), name="member-list-role"),
    path("member-branch", AddMemberBranch.as_view(), name="member-create-role"),
    path(
        "member-branch/<int:pk>",
        MemberBranchDetail.as_view(),
        name="member-detail-role",
    ),
    path("user/<int:pk>/profile", UserProfile.as_view(), name="profile-list"),
    path("profile/<int:pk>", ProfileDetail.as_view(), name="profile-detail"),
    path("login", LoginView.as_view(), name="s_login"),
    path("logout", LogoutView.as_view(), name="s_logout"),
    path("user/update-password", UpdatePassword.as_view(), name="update-password"),
    path(
        "user/reset-password",
        ResetPasswordRequestCode.as_view(),
        name="reset-password-request",
    ),
    path(
        "user/reset-password/<str:code>/",
        ResetPasswordConfirm.as_view(),
        name="reset-password-confirm",
    ),
    path(
        "member/<int:pk>/toggle-approval",
        ToggleMemberApprovalView.as_view(),
        name="member-approval-toggle",
    ),
]
