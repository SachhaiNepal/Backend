from django.db import models
from django.core.exceptions import ValidationError


from accounts.sub_models.member import Member
from utils.constants import MEMBER_ROLE_CHOICES


class MemberRole(models.Model):
    member = models.ForeignKey(
        Member, on_delete=models.CASCADE, related_name="member_roles"
    )
    role_name = models.CharField(max_length=18, choices=MEMBER_ROLE_CHOICES)
    from_date = models.DateField()
    to_date = models.DateField()
    member_branch = models.ForeignKey("MemberBranch", on_delete=models.CASCADE, related_name="member_branch_roles")

    class Meta:
        verbose_name = "Member Role"
        verbose_name_plural = "Member Roles"
        unique_together = ("member", "role_name", "member_branch")

    def clean(self):
        if self.member_branch.date_of_membership > self.from_date:
            raise ValidationError("Role period should be within the date of membership.")
        if self.from_date > self.to_date or self.from_date == self.to_date:
            raise ValidationError("To date must be smaller than from date.")
        if self.member_branch.member != self.member:
            raise ValidationError("Please assign member branch of the same member.")

    def __str__(self):
        return "{}: {}".format(self.member.user.username, self.role_name)
