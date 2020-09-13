from django.contrib import admin
from django.utils import timezone

from multimedia.models import *


def save_form_set(self, request, form, formset, change):
    if formset.model == Multimedia:
        instances = formset.save(commit=False)
        for instance in instances:
            instance.updated_by = request.user
            if instance.is_approved:
                instance.approved_by = request.user
                instance.approved_at = timezone.now()
            instance.save()
    else:
        formset.save()


class MultimediaVideoAdmin(admin.StackedInline):
    model = MultimediaVideo
    fk_name = "multimedia"
    extra = 0
    min_num = 1
    max_num = 10
    can_delete = True
    verbose_name_plural = "Add Multimedia Video"


class MultimediaAudioAdmin(admin.StackedInline):
    model = MultimediaAudio
    fk_name = "multimedia"
    extra = 0
    min_num = 1
    max_num = 10
    can_delete = True
    verbose_name_plural = "Add Multimedia Audio"


class MultimediaImageAdmin(admin.StackedInline):
    model = MultimediaImage
    fk_name = "multimedia"
    extra = 0
    min_num = 1
    max_num = 10
    can_delete = True
    verbose_name_plural = "Add Multimedia Image"


@admin.register(Multimedia)
class MultimediaAdmin(admin.ModelAdmin):
    inlines = [MultimediaVideoAdmin, MultimediaAudioAdmin, MultimediaImageAdmin]

    list_display = ("title", "is_approved", "approved_at", "approved_by", "uploaded_by", "uploaded_at")

    fieldsets = (
        ("Media Information", {
            "classes": ("wide", "extrapretty"),
            "fields": ("title", "description")
        }),
        ("Business Information", {
            "classes": ("wide",),
            "fields": ("is_approved",)
        })
    )

    list_filter = ("is_approved", "uploaded_at", "approved_at",)
    search_fields = ("approved_by", "uploaded_by", "title", "description", "audio", "video")
    date_hierarchy = "uploaded_at"
    ordering = ("title", "is_approved", "approved_at", "approved_by", "uploaded_by", "uploaded_at")
    list_per_page = 10

    def save_model(self, request, obj, form, change):
        obj.uploaded_by = request.user
        if obj.is_approved:
            obj.approved_by = request.user
            obj.approved_at = timezone.now()
        obj.save()

    def save_formset(self, request, form, formset, change):
        save_form_set(self, request, form, formset, change)


class ArticleImageAdmin(admin.StackedInline):
    model = ArticleImage
    fk_name = "article"
    extra = 0
    min_num = 1
    max_num = 10
    can_delete = True
    verbose_name_plural = "Add Article Image"


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ArticleImageAdmin]

    list_display = ("title", "is_approved", "approved_at", "approved_by", "uploaded_by", "uploaded_at")
    list_filter = (
        ("is_approved", admin.BooleanFieldListFilter),
        "approved_at",
        "uploaded_at",
    )
    list_per_page = 10
    search_fields = ("title", "approved_by__name", "uploaded_by__name")

    # update form for admin site
    fieldsets = (
        ("Article Information.", {
            "classes": ("wide", "extrapretty"),
            "fields": ("title", "description")
        }),

        ("Business Details", {
            "classes": ("wide", "extrapretty"),
            "fields": ("is_approved",)
        })
    )

    def save_model(self, request, obj, form, change):
        obj.uploaded_by = request.user
        if obj.is_approved:
            obj.approved_by = request.user
            obj.approved_at = timezone.now()
        obj.save()

    def save_formset(self, request, form, formset, change):
        save_form_set(self, request, form, formset, change)


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
        ("Media Information.", {
            "classes": ("wide", "extrapretty"),
            "fields": ("article", "multimedia")
        }),

        ("Comment Details", {
            "classes": ("wide", "extrapretty"),
            "fields": ("comment", "reply_to")
        })
    )
    search_fields = ("writer", "article", "multimedia", "comment", "reply_to")
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
        ("Media Information.", {
            "classes": ("wide", "extrapretty"),
            "fields": ("article", "multimedia")
        }),

        ("Love Information", {
            "classes": ("wide", "extrapretty"),
            "fields": ("is_loved",)
        })
    )
    search_fields = ("lover", "article", "multimedia", "is_loved")
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
