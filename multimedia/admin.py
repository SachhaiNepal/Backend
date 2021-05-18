from django.contrib import admin
from django.utils import timezone

from multimedia.sub_models.article_media import ArticleImage
from multimedia.sub_models.multimedia_media import MultimediaVideo, MultimediaAudio, MultimediaImage
from multimedia.sub_models.post import Article, Multimedia
from multimedia.sub_models.post_action import PinMedia, BookmarkMedia, Love, Comment


class MultimediaVideoAdmin(admin.StackedInline):
    model = MultimediaVideo
    fk_name = "multimedia"
    extra = 0
    min_num = 0
    max_num = 5
    can_delete = True
    verbose_name_plural = "Add Multimedia Video"


class MultimediaAudioAdmin(admin.StackedInline):
    model = MultimediaAudio
    fk_name = "multimedia"
    extra = 0
    min_num = 0
    max_num = 5
    can_delete = True
    verbose_name_plural = "Add Multimedia Audio"


class MultimediaImageAdmin(admin.StackedInline):
    model = MultimediaImage
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
        "uploaded_at",
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
        "uploaded_at",
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
    date_hierarchy = "uploaded_at"
    ordering = (
        "title",
        "is_approved",
        "approved_at",
        "approved_by",
        "uploaded_by",
        "uploaded_at",
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
        images = MultimediaImage.objects.filter(multimedia=obj)
        if images.count() > 0:
            for image in images:
                image.delete()
        audios = MultimediaAudio.objects.filter(multimedia=obj)
        if audios.count() > 0:
            for audio in audios:
                audio.delete()
        videos = MultimediaVideo.objects.filter(multimedia=obj)
        if videos.count() > 0:
            for video in videos:
                video.delete()
        super().delete_model(request, obj)


class ArticleImageAdmin(admin.StackedInline):
    model = ArticleImage
    fk_name = "article"
    extra = 0
    min_num = 0
    max_num = 10
    can_delete = True
    verbose_name_plural = "Add Article Image"


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ArticleImageAdmin]

    list_display = (
        "title",
        "is_approved",
        "approved_at",
        "approved_by",
        "uploaded_by",
        "uploaded_at",
    )
    list_filter = (
        ("is_approved", admin.BooleanFieldListFilter),
        "approved_at",
        "uploaded_at",
    )
    list_per_page = 10
    search_fields = (
        "title",
        "approved_by__username",
        "approved_by__email",
        "uploaded_by__username",
        "uploaded_by__email",
    )

    # update form for admin site
    fieldsets = (
        (
            "Article Information",
            {"classes": ("wide", "extrapretty"), "fields": ("title", "description")},
        ),
        (
            "Business Details",
            {"classes": ("wide", "extrapretty"), "fields": ("is_approved",)},
        ),
    )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.uploaded_by = request.user
            if obj.is_approved:
                obj.approved_by = request.user
                obj.approved_at = timezone.now()
        if change:
            this_record = Article.objects.get(pk=obj.pk)
            if this_record.is_approved and not obj.is_approved:
                obj.approved_by = None
                obj.approved_at = None
            if not this_record.is_approved and obj.is_approved:
                obj.approved_by = request.user
                obj.approved_at = timezone.now()
        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        images = ArticleImage.objects.filter(article=obj)
        if images.count() > 0:
            for image in images:
                image.delete()
        super().delete_model(request=request, obj=obj)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "writer",
        "comment",
        "article",
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
    autocomplete_fields = ("article", "multimedia")
    fieldsets = (
        (
            "Media Information",
            {"classes": ("wide", "extrapretty"), "fields": ("article", "multimedia")},
        ),
        (
            "Comment Details",
            {"classes": ("wide", "extrapretty"), "fields": ("comment", "reply_to")},
        ),
    )
    search_fields = (
        "writer__username",
        "writer__email",
        "article__title",
        "multimedia__title",
        "comment",
        "reply_to__comment",
    )
    date_hierarchy = "created_at"
    ordering = (
        "writer",
        "comment",
        "article",
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
        "article",
        "multimedia",
        "created_at",
        "updated_at",
    )
    list_filter = (
        "created_at",
        "updated_at",
    )
    list_per_page = 10
    autocomplete_fields = ("article", "multimedia")
    fieldsets = (
        (
            "Media Information",
            {"classes": ("wide", "extrapretty"), "fields": ("article", "multimedia")},
        ),
        (
            "Love Information",
            {"classes": ("wide", "extrapretty"), "fields": ("is_loved",)},
        ),
    )
    search_fields = (
        "lover__username",
        "lover__email",
        "article__title",
        "multimedia__title",
    )
    date_hierarchy = "created_at"
    ordering = (
        "lover",
        "is_loved",
        "article",
        "multimedia",
        "created_at",
        "updated_at",
    )

    def save_model(self, request, obj, form, change):
        obj.lover = request.user
        obj.save()


@admin.register(BookmarkMedia)
class BookmarkMediaAdmin(admin.ModelAdmin):
    list_display = ("article", "multimedia", "is_bookmarked", "marker", "timestamp")
    ordering = ("article", "multimedia", "is_bookmarked", "marker", "timestamp")
    date_hierarchy = "timestamp"
    list_filter = ("is_bookmarked", "timestamp")
    autocomplete_fields = ("article", "multimedia")
    fieldsets = (
        (
            "Media Information",
            {"classes": ("wide", "extrapretty"), "fields": ("article", "multimedia")},
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


@admin.register(PinMedia)
class PinMediaAdmin(admin.ModelAdmin):
    list_display = ("article", "multimedia", "is_pinned", "pinner", "timestamp")
    ordering = ("article", "multimedia", "is_pinned", "pinner", "timestamp")
    date_hierarchy = "timestamp"
    list_filter = ("is_pinned", "timestamp")
    autocomplete_fields = ("article", "multimedia")
    fieldsets = (
        (
            "Media Information",
            {"classes": ("wide", "extrapretty"), "fields": ("article", "multimedia")},
        ),
        (
            "Bookmark Information",
            {"classes": ("wide", "extrapretty"), "fields": ("is_pinned",)},
        ),
    )
    search_fields = (
        "pinner__username",
        "pinner__email",
        "article__title",
        "multimedia__title",
    )

    def save_model(self, request, obj, form, change):
        obj.pinner = request.user
        obj.save()


admin.site.register(MultimediaImage)
admin.site.register(MultimediaVideo)
admin.site.register(MultimediaAudio)
admin.site.register(ArticleImage)
