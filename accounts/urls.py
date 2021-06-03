from django.urls import path
from rest_framework.routers import DefaultRouter

from accounts.views.login import LoginView, LogoutView
from accounts.views.member import (ListMember, MemberDetail, MemberFilterView,
                                   ToggleMemberApprovalView)
from accounts.views.member_branch import ListMemberBranch, MemberBranchViewSet
from accounts.views.member_role import ListMemberRole, MemberRoleDetail
from accounts.views.password import (ConfirmResetPassword,
                                     ResetPasswordRequestCode, UpdatePassword)
from accounts.views.profile import (ProfileDetail, ProfileImageViewSet,
                                    UserProfile)
from accounts.views.register_follower import RegisterFollower
from accounts.views.user_permission import (ListUserPermission,
                                            UserPermissionDetail)
from accounts.views.users import ListFollower, ListUsersView, UserDetail

app_name = "accounts"

router = DefaultRouter()
router.register(r"profile-image", ProfileImageViewSet, basename="profile-image")
router.register(r"member-branch", MemberBranchViewSet, basename="profile-image")
urlpatterns = router.urls

urlpatterns += [
    path("register-follower", RegisterFollower.as_view(), name="register-follower"),
    path("user", ListFollower.as_view(), name="users-list"),
    path("user/<int:pk>", UserDetail.as_view(), name="user-detail"),
    path("member", ListMember.as_view(), name="members-list"),
    path("member/<int:pk>", MemberDetail.as_view(), name="member-detail"),
    path("member/<int:pk>/role", ListMemberRole.as_view(), name="member-role-list"),
    path("member-role/<int:pk>", MemberRoleDetail.as_view(), name="member-role-detail"),
    path(
        "member/<int:pk>/branch", ListMemberBranch.as_view(), name="member-branch-list"
    ),
    # path("member-branch/<int:pk>", MemberBranchDetail.as_view(), name="member-branch-detail"),
    path(
        "member/<int:pk>/toggle-approval",
        ToggleMemberApprovalView.as_view(),
        name="member-toggle-approval",
    ),
    path("user/<int:pk>/profile", UserProfile.as_view(), name="profile-list"),
    path("profile/<int:pk>", ProfileDetail.as_view(), name="profile-detail"),
    path("login", LoginView.as_view(), name="user-login"),
    path("logout", LogoutView.as_view(), name="user-logout"),
    path("update-password", UpdatePassword.as_view(), name="update-password"),
    path(
        "reset-password",
        ResetPasswordRequestCode.as_view(),
        name="reset-password-request",
    ),
    path(
        "reset-password/<str:code>/",
        ConfirmResetPassword.as_view(),
        name="confirm-reset-password",
    ),
    path("user-permission", ListUserPermission.as_view(), name="user-permission"),
    path("magic/<int:pk>", UserPermissionDetail.as_view(), name="magic"),
    path("list-user", ListUsersView.as_view(), name="user-filter"),
    path("list-member", MemberFilterView.as_view(), name="member-filter"),
]
