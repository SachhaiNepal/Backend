from django.contrib.auth import get_user_model
from django.db import models


class Member(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False, editable=False)
    approved_by = models.ForeignKey(
        get_user_model(),
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING,
        related_name="approved_members",
        editable=False,
    )
    approved_at = models.DateTimeField(
        default=None, null=True, blank=True, editable=False
    )
    created_by = models.ForeignKey(
        get_user_model(),
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING,
        related_name="members_created",
        editable=False,
    )
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_by = models.ForeignKey(
        get_user_model(),
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING,
        related_name="members_updated",
        editable=False,
    )
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        verbose_name_plural = "Members"
        permissions = [
            ("can_approve_member", "Can toggle Member Approval Status"),
        ]

    def __str__(self):
        return self.user.username
