from django.db import models

from accounts.sub_models.member import Member
from branch.models import Branch


class MemberBranch(models.Model):
    member = models.ForeignKey(
        Member, on_delete=models.DO_NOTHING, related_name="member_branches"
    )
    branch = models.ForeignKey(Branch, models.CASCADE, related_name="member_branch")
    date_of_membership = models.DateField()

    class Meta:
        verbose_name = "Member Branch"
        verbose_name_plural = "Member Branches"
        unique_together = ("member", "branch")

    def __str__(self):
        return "{}: {}".format(self.member.user.username, self.branch.name)
