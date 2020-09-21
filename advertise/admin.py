from django.contrib import admin
from advertise.models import Advertisement


class AdvertisementAdmin(admin.ModelAdmin):
    list_display = (
        "owner",
        "heading",
        "description",
        "created_by",
        "created_at",
        "modified_by",
        "modified_at",
    )

    search_fields = (
        "heading",
        "description",
        "owner",
        "created_by",
        "modified_by",
    )
    list_filter = (
        "created_at",
        "modified_at",
    )
    date_hierarchy = "created_at"
    fieldsets = (
        (" Advertisement Information", {
            "classes": ("wide", "extrapretty"),
            "fields": (
                "owner",
                "heading",
                "description",
                "image",
            )
        }),
    )
    ordering = (
        "heading",
        "description",
        "image",
        "owner",
        "created_at",
        "modified_at",
        "created_by",
        "modified_by",
    )
    list_per_page = 10

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.modified_by = request.user
        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        obj.image.delete()
        obj.delete()


admin.site.register(Advertisement, AdvertisementAdmin)
