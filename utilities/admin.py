from django.contrib import admin
from django.core.exceptions import ValidationError

from backend.settings import MAX_SHOWCASE_GALLERY_IMAGES

from utilities.models import (
    AboutUs, AboutUsImage, Service,
    SliderImage, ShowcaseGalleryImage, ServiceImage, Feedback, FeedbackFile, ContactUs
)


class SliderImageAdmin(admin.ModelAdmin):
    list_display = ("image", "title", "context", "subtitle", "timestamp")
    search_fields = ("title", "context", "subtitle")
    list_filter = ["timestamp"]
    date_hierarchy = "timestamp"
    fieldsets = (
        ("Slider Image", {"classes": ("wide", "extrapretty"), "fields": ("image",)}),
        (
            "Slider Image Information",
            {
                "classes": ("wide", "extrapretty"),
                "fields": ("title", "context", "subtitle"),
            },
        ),
    )
    ordering = ("image", "title", "context", "subtitle")

    def save_model(self, request, obj, form, change):
        if not change:
            if SliderImage.objects.count() >= 1:
                raise ValidationError(
                    "Only one slider image can be created. Please update the existing"
                    " one. You can also delete existing item to add a new one."
                )
        super(SliderImageAdmin, self).save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        obj.image.delete()
        super().delete_model(request, obj)


class ShowcaseGalleryImageAdmin(admin.ModelAdmin):
    search_fields = ("image.name", "heading")
    list_filter = ["heading", "content", "image", "timestamp"]
    date_hierarchy = "timestamp"
    fieldsets = (
        (
            "Slider Image", {
                "classes": (
                    "wide", "extrapretty"
                ),
                "fields": (
                    "image", "heading", "content"
                )
            }
        ),
    )
    ordering = ("timestamp",)

    def save_model(self, request, obj, form, change):
        if not change:
            if ShowcaseGalleryImage.objects.count() >= MAX_SHOWCASE_GALLERY_IMAGES:
                raise ValidationError(
                    "Maximum instance count reached."
                    f" Only ${MAX_SHOWCASE_GALLERY_IMAGES} items can be created for this model." +
                    " Please update the existing ones."
                    " You can also delete existing item to add a new one."
                )
        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        obj.image.delete()
        super().delete_model(request, obj)


class ServiceAdmin(admin.ModelAdmin):
    search_fields = ("title", "description", "timestamp")
    list_filter = ["timestamp"]
    date_hierarchy = "timestamp"
    fieldsets = (
        (
            "Service Information",
            {
                "classes": ("wide", "extrapretty"),
                "fields": (
                    "title",
                    "description",
                ),
            },
        ),
        ("Service Media", {"classes": ("wide", "extrapretty"), "fields": ("video_url",)}),
    )
    ordering = ("timestamp",)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.writer = request.user
        super().save_model(request, obj, form, change)


class ServiceImageAdmin(admin.ModelAdmin):
    list_display = ["image"]
    list_filter = ["timestamp"]
    date_hierarchy = "timestamp"

    def delete_model(self, request, obj):
        obj.image.delete()
        super().delete_model(request, obj)


class AboutUsImageAdmin(admin.ModelAdmin):
    list_display = ["image"]
    list_filter = ["timestamp"]
    date_hierarchy = "timestamp"

    def delete_model(self, request, obj):
        obj.image.delete()
        super().delete_model(request, obj)


class AboutUsAdmin(admin.ModelAdmin):
    list_display = ["about_us", "video_url", "timestamp"]
    list_filter = ["timestamp"]
    date_hierarchy = "timestamp"

    def save_model(self, request, obj, form, change):
        if not change:
            if AboutUs.objects.count() >= 1:
                raise ValidationError(
                    "Only one item can be created. Please update the existing"
                    " one. You can also delete existing item to add a new one."
                )
        super().save_model(request, obj, form, change)


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ["subject", "message", "writer", "seen", "reply_to", "timestamp"]
    list_filter = ["timestamp", "seen"]
    search_fields = ["subject", "message", "writer__username"]
    date_hierarchy = "timestamp"

    def save_model(self, request, obj, form, change):
        if not change:
            obj.writer = request.user
        super().save_model(request, obj, form, change)


class FeedbackFileAdmin(admin.ModelAdmin):
    list_display = ["file", "timestamp"]
    list_filter = ["timestamp", "feedback"]
    search_fields = ["feedback__subject", "feedback__writer__username"]
    date_hierarchy = "timestamp"
    autocomplete_fields = ["feedback"]

    def delete_model(self, request, obj):
        obj.file.delete()
        super().delete_model(request, obj)


class ContactUsAdmin(admin.ModelAdmin):
    list_display = ["contacts", "emails", "timestamp"]

    def save_model(self, request, obj, form, change):
        if not change:
            if AboutUs.objects.count() >= 1:
                raise ValidationError(
                    "Only one item can be created. Please update the existing"
                    " one. You can also delete existing item to add a new one."
                )
        super().save_model(request, obj, form, change)


admin.site.register(SliderImage, SliderImageAdmin)
admin.site.register(ShowcaseGalleryImage, ShowcaseGalleryImageAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(ServiceImage, ServiceImageAdmin)
admin.site.register(AboutUs, AboutUsAdmin)
admin.site.register(AboutUsImage, AboutUsImageAdmin)
admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(FeedbackFile, FeedbackFileAdmin)
admin.site.register(ContactUs, ContactUsAdmin)
