from django.contrib import admin
from django.utils import timezone

from multimedia.sub_models.action import Bookmark, Comment, Love
from multimedia.sub_models.media import Image, Sound, Video, VideoUrl
from multimedia.sub_models.multimedia import Multimedia


class MultimediaVideoAdmin(admin.StackedInline):
    model = Video
    fk_name = "multimedia"
    extra = 0
    min_num = 0
    max_num = 5
    can_delete = True
    verbose_name_plural = "Add Multimedia Video"


class MultimediaAudioAdmin(admin.StackedInline):
    model = Sound
    fk_name = "multimedia"
    extra = 0
    min_num = 0
    max_num = 5
    can_delete = True
    verbose_name_plural = "Add Multimedia Audio"


class MultimediaImageAdmin(admin.StackedInline):
    model = Image
    fk_name = "multimedia"
    extra = 0
    min_num = 0
    max_num = 10
    can_delete = True
    verbose_name_plural = "Add Multimedia Image"


@admin.register(Multimedia)
class MultimediaAdmin(admin.ModelAdmin):
    inlines = [MultimediaAudioAdmin, MultimediaImageAdmin, MultimediaVideoAdmin]

    list_display = (
        "title",
        "is_approved",
        "approved_at",
        "approved_by",
        "uploaded_by",
        "timestamp",
    )

    fieldsets = (
        (
            "Media Information",
            {"classes": ("wide", "extrapretty"), "fields": ("title", "description")},
        ),
        ("Business Information", {"classes": ("wide",), "fields": ("is_approved",)}),
    )

    list_filter = (
        "is_approved",
        "timestamp",
        "approved_at",
    )
    search_fields = (
        "approved_by__username",
        "approved_by__email",
        "uploaded_by__username",
        "uploaded_by__email",
        "title",
        "description",
    )
    date_hierarchy = "timestamp"
    ordering = (
        "title",
        "is_approved",
        "approved_at",
        "approved_by",
        "uploaded_by",
        "timestamp",
    )
    list_per_page = 10

    def save_model(self, request, obj, form, change):
        if not change:
            obj.uploaded_by = request.user
            if obj.is_approved:
                obj.approved_by = request.user
                obj.approved_at = timezone.now()
        if change:
            this_record = Multimedia.objects.get(pk=obj.pk)
            if this_record.is_approved and not obj.is_approved:
                obj.approved_by = None
                obj.approved_at = None
            if not this_record.is_approved and obj.is_approved:
                obj.approved_by = request.user
                obj.approved_at = timezone.now()
        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        images = Image.objects.filter(multimedia=obj)
        if images.count() > 0:
            for image in images:
                image.delete()
        audios = Sound.objects.filter(multimedia=obj)
        if audios.count() > 0:
            for sound in audios:
                sound.delete()
        videos = Video.objects.filter(multimedia=obj)
        if videos.count() > 0:
            for video in videos:
                video.delete()
        super().delete_model(request, obj)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "writer",
        "comment",
        "multimedia",
        "reply_to",
        "created_at",
        "updated_at",
    )
    list_filter = (
        "created_at",
        "updated_at",
    )
    list_per_page = 10
    autocomplete_fields = ("multimedia",)
    search_fields = (
        "writer__username",
        "writer__email",
        "multimedia__title",
        "comment",
        "reply_to__comment",
    )
    date_hierarchy = "created_at"
    ordering = (
        "writer",
        "comment",
        "multimedia",
        "reply_to",
        "created_at",
        "updated_at",
    )

    def save_model(self, request, obj, form, change):
        obj.writer = request.user
        obj.save()


@admin.register(Love)
class LoveAdmin(admin.ModelAdmin):
    list_display = (
        "lover",
        "is_loved",
        "multimedia",
        "created_at",
        "updated_at",
    )
    list_filter = (
        "created_at",
        "updated_at",
    )
    list_per_page = 10
    autocomplete_fields = ("multimedia",)
    fieldsets = (
        (
            "Media Information",
            {"classes": ("wide", "extrapretty"), "fields": ("multimedia",)},
        ),
        (
            "Love Information",
            {"classes": ("wide", "extrapretty"), "fields": ("is_loved",)},
        ),
    )
    search_fields = (
        "lover__username",
        "lover__email",
        "multimedia__title",
    )
    date_hierarchy = "created_at"
    ordering = (
        "lover",
        "is_loved",
        "multimedia",
        "created_at",
        "updated_at",
    )

    def save_model(self, request, obj, form, change):
        obj.lover = request.user
        obj.save()


@admin.register(Bookmark)
class BookmarkMediaAdmin(admin.ModelAdmin):
    list_display = ("multimedia", "is_bookmarked", "marker", "timestamp")
    ordering = ("multimedia", "is_bookmarked", "marker", "timestamp")
    date_hierarchy = "timestamp"
    list_filter = ("is_bookmarked", "timestamp")
    autocomplete_fields = ("multimedia",)
    fieldsets = (
        (
            "Media Information",
            {"classes": ("wide", "extrapretty"), "fields": ("multimedia",)},
        ),
        (
            "Bookmark Information",
            {"classes": ("wide", "extrapretty"), "fields": ("is_bookmarked",)},
        ),
    )
    search_fields = (
        "marker__username",
        "marker__email",
        "article__title",
        "multimedia__title",
    )

    def save_model(self, request, obj, form, change):
        obj.marker = request.user
        obj.save()


admin.site.register(Image)
admin.site.register(Video)
admin.site.register(VideoUrl)
admin.site.register(Sound)
