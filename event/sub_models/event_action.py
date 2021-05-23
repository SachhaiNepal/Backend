from django.db import models

from accounts.sub_models.member import Member
from event.sub_models.event import Event


class EventInterest(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="interested_event",
    )
    member = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        related_name="interested_members",
    )
    going = models.BooleanField(default=False)
    interested = models.BooleanField(default=False)
    attended = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}: {}".format(self.member.user.username, self.event.name)

    class Meta:
        verbose_name = "Interested Event"
        verbose_name_plural = "Interested Events"
        ordering = ["-created_at"]


class EventComment(models.Model):
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name="event_comments", editable=False
    )
    writer = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        related_name="member_event_comments",
        editable=False,
    )
    comment = models.CharField(max_length=1024)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}: {}".format(self.member.user.username, self.event.name)

    class Meta:
        verbose_name = "Going Event"
        verbose_name_plural = "Going Events"
        ordering = ["-created_at"]
