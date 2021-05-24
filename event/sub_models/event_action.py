from django.contrib.auth import get_user_model
from django.db import models

from event.sub_models.event import Event


class EventInterest(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="interested_event",
    )
    follower = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="interested_followers",
    )
    going = models.BooleanField(default=False)
    interested = models.BooleanField(default=False)
    attended = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}: {}".format(self.follower.username, self.event.name)

    class Meta:
        verbose_name = "Interested Event"
        verbose_name_plural = "Interested Events"
        ordering = ["-created_at"]


class EventComment(models.Model):
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name="event_comments", editable=False
    )
    writer = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="follower_event_comments",
        editable=False,
    )
    comment = models.CharField(max_length=1024)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}: {}".format(self.follower.username, self.event.name)

    class Meta:
        verbose_name = "Going Event"
        verbose_name_plural = "Going Events"
        ordering = ["-created_at"]
