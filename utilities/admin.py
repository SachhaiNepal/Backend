from django.contrib import admin
from django.core.exceptions import ValidationError

from backend.settings import MAX_SHOWCASE_GALLERY_IMAGES
from utilities.models import (
    AboutUs,
    AboutUsImage,
    Service,
    ShowcaseGallery,
    ShowcaseSlider,
)


class ShowcaseSliderAdmin(admin.ModelAdmin):
    list_display = ("image", "title", "context", "subtitle", "created_at")
    search_fields = ("title", "context", "subtitle")
    list_filter = ["created_at"]
    date_hierarchy = "created_at"
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

    def save_model(self, *args, **kwargs):
        if ShowcaseSlider.objects.count() >= 3:
            raise ValidationError(
                "Only {} slider images are allowed to save.".format(3)
            )
        super(ShowcaseSliderAdmin, self).save_model(*args, **kwargs)

    def delete_model(self, request, obj):
        obj.image.delete()
        obj.delete()


class ShowcaseGalleryAdmin(admin.ModelAdmin):
    search_fields = ("image.name",)
    list_filter = ["created_at"]
    date_hierarchy = "created_at"
    fieldsets = (
        ("Slider Image", {"classes": ("wide", "extrapretty"), "fields": ("image",)}),
    )
    ordering = ("image", "created_at")

    def save_model(self, *args, **kwargs):
        if ShowcaseGallery.objects.count() >= MAX_SHOWCASE_GALLERY_IMAGES:
            raise ValidationError(
                "Only {} images are allowed to save.".format(
                    MAX_SHOWCASE_GALLERY_IMAGES
                )
            )
        super(ShowcaseGalleryAdmin, self).save_model(*args, **kwargs)

    def delete_model(self, request, obj):
        obj.image.delete()
        obj.delete()


class ServiceAdmin(admin.ModelAdmin):
    search_fields = ("title", "description", "image", "created_at")
    list_filter = ["created_at"]
    date_hierarchy = "created_at"
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
        ("Service Media", {"classes": ("wide", "extrapretty"), "fields": ("image",)}),
    )
    ordering = ("title", "created_at")

    def delete_model(self, request, obj):
        obj.image.delete()
        obj.delete()


class AboutUsImageAdmin(admin.ModelAdmin):
    def delete_model(self, request, obj):
        obj.image.delete()
        obj.delete()


class AboutUsAdmin(admin.ModelAdmin):
    def save_model(self, *args, **kwargs):
        if AboutUs.objects.count() >= 1:
            raise ValidationError("Single object model. Multiple instance not allowed")
        super(AboutUsAdmin, self).save_model(*args, **kwargs)


admin.site.register(ShowcaseSlider, ShowcaseSliderAdmin)
admin.site.register(ShowcaseGallery, ShowcaseGalleryAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(AboutUs, AboutUsAdmin)
admin.site.register(AboutUsImage, AboutUsImageAdmin)
