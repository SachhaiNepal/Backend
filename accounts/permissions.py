from rest_framework import permissions


class CanApproveMember(permissions.BasePermission):
    def has_permission(self, request, view):
        performer = request.user
        return performer.has_perm("accounts.can_approve_member")
