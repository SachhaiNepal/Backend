from django.core.exceptions import ValidationError
from django.db import models

from accounts.sub_models.member import Member
from branch.models import Branch


class MemberBranch(models.Model):
    member = models.ForeignKey(
        Member, on_delete=models.DO_NOTHING, related_name="member_branches"
    )
    branch = models.PositiveBigIntegerField()
    date_of_membership = models.DateField()

    class Meta:
        verbose_name = "Member Branch"
        verbose_name_plural = "Member Branches"
        unique_together = ("member", "branch")

    def __str__(self):
        return self.member.user.username

    def clean(self):
        selected_branch = self.branch
        # check if selected branch id is valid
        try:
            Branch.objects.get(pk=selected_branch)
        except Branch.DoesNotExist:
            raise ValidationError("Selected branch does not exist.")
