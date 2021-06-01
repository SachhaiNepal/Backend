from django.contrib import admin
from django.utils import timezone

from event.sub_models.event import Event
from event.sub_models.event_action import EventComment, EventInterest
from event.sub_models.event_media import EventPhoto, EventVideo, EventVideoUrl


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "venue",
        "branch",
        "start_date",
        "duration",
        "time_of_day",
        "type",
        "is_main",
        "is_approved",
        "approved_at",
        "approved_by",
        "created_at",
        "created_by",
        "updated_at",
        "updated_by",
    )

    fieldsets = (
        (
            "Event Information",
            {
                "classes": ("wide", "extrapretty"),
                "fields": (
                    "title",
                    "description",
                    "branch",
                    "contact",
                    "venue",
                    "start_date",
                    "duration",
                    "time_of_day",
                    "type",
                    "is_main",
                    "is_approved",
                ),
            },
        ),
        (
            "Location Information",
            {
                "classes": ("wide", "extrapretty"),
                "fields": (
                    "country",
                    "province",
                    "district",
                    "municipality",
                    "municipality_ward",
                    "vdc",
                    "vdc_ward",
                ),
            },
        ),
    )

    list_filter = ("is_approved", "created_at", "approved_at", "is_main")
    search_fields = (
        "approved_by__username",
        "approved_by__email",
        "created_by__username",
        "created_by__email",
        "title",
        "description",
    )
    date_hierarchy = "created_at"
    ordering = (
        "title",
        "venue",
        "start_date",
        "duration",
        "time_of_day",
        "type",
        "is_approved",
        "approved_at",
        "approved_by",
        "created_by",
        "created_at",
        "updated_at",
        "updated_by",
    )
    list_per_page = 10

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
            obj.updated_by = request.user
            if obj.is_approved:
                obj.approved_by = request.user
                obj.approved_at = timezone.now()
        if change:
            obj.updated_by = request.user
            this_record = Event.objects.get(pk=obj.pk)
            if this_record.is_approved and not obj.is_approved:
                obj.approved_by = None
                obj.approved_at = None
            if not this_record.is_approved and obj.is_approved:
                obj.approved_by = request.user
                obj.approved_at = timezone.now()
        super().save_model(request, obj, form, change)


admin.site.register(EventPhoto)
admin.site.register(EventVideo)
admin.site.register(EventVideoUrl)
admin.site.register(EventInterest)
admin.site.register(EventComment)
