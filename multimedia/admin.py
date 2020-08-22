from django.contrib import admin
from django.db.models.functions import datetime

from multimedia.models import Multimedia, ArticleImage, Article


@admin.register(Multimedia)
class MultimediaAdmin(admin.ModelAdmin):
    list_display = ("title", "is_approved", "approved_at", "approved_by", "uploaded_by", "uploaded_at")

    fieldsets = (
        ("Media Information", {
            "classes": ("wide", "extrapretty"),
            "fields": ("title", "description")
        }),
        ("Media Files", {
            "classes": ("wide", "extrapretty"),
            "fields": ("video", "audio")
        }),
        ("Business Information", {
            "classes": ("wide",),
            "fields": ("is_approved",)
        })
    )

    list_filter = ("is_approved",)
    search_fields = ("approved_by", "uploaded_by", "title", "description", "audio", "video")
    date_hierarchy = "uploaded_at"
    ordering = ("title", "is_approved", "approved_at", "approved_by", "uploaded_by", "uploaded_at")

    def save_model(self, request, obj, form, change):
        obj.uploaded_by = request.user
        if obj.is_approved:
            obj.approved_by = request.user
        obj.save()

    def save_formset(self, request, form, formset, change):
        if formset.model == Multimedia:
            instances = formset.save(commit=False)
            for instance in instances:
                instance.updated_by = request.user
                if instance.is_approved:
                    instance.approved_by = request.user
                instance.save()
        else:
            formset.save()


class ArticleImageAdmin(admin.StackedInline):
    model = ArticleImage
    fk_name = "article"


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ArticleImageAdmin]

    list_display = ("title", "is_approved", "approved_at", "approved_by", "uploaded_by", "uploaded_at")
    list_filter = (
        ("is_approved", admin.BooleanFieldListFilter),
    )

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
            obj.approved_at = datetime.datetime.now()
        obj.save()

    def save_formset(self, request, form, formset, change):
        if formset.model == Article:
            instances = formset.save(commit=False)
            for instance in instances:
                instance.updated_by = request.user
                if instance.is_approved:
                    instance.approved_by = request.user
                    instance.approved_at = datetime.datetime.now()
                instance.save()
        else:
            formset.save()
