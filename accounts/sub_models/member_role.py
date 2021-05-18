from django.db import models

from accounts.sub_models.member import Member
from accounts.sub_models.member_branch import MemberBranch
from branch.models import Branch
from utils.constants import MEMBER_ROLE_CHOICES


class MemberRole(models.Model):
    member = models.ForeignKey(
        Member, on_delete=models.CASCADE, related_name="member_role"
    )
    role_name = models.CharField(max_length=18, choices=MEMBER_ROLE_CHOICES)
    from_date = models.DateField()
    to_date = models.DateField()
    branch = models.PositiveBigIntegerField()

    class Meta:
        verbose_name = "Member Role"
        verbose_name_plural = "Member Roles"
        unique_together = ("member", "role_name", "branch")

    def clean(self):
        selected_member = self.member
        selected_branch = self.branch
        # check if selected branch id is valid
        try:
            Branch.objects.get(pk=selected_branch)
        except Branch.DoesNotExist:
            raise ValidationError("Selected branch does not exist.")
        # check if member is registered in selected branch
        member_branches = MemberBranch.objects.filter(member=selected_member)
        found = False
        for member_branch in member_branches:
            if member_branch.id == selected_branch:
                found = True
        if not found:
            raise ValidationError("Member not registered in selected branch.")

    def __str__(self):
        return self.member.user.username
