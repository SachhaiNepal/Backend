from django.contrib import admin

from multimedia.models import Multimedia


class MultimediaAdmin(admin.ModelAdmin):
    list_display = ("title", "is_approved", "approved_at", "approved_by", "uploaded_by", "uploaded_at")

    buffer_field_sets = (
        ("Media Information", {
            "classes": ("wide",),
            "fields": ("title", "description")
        }),
        ("Media Files", {
            "classes": ("wide",),
            "fields": ("video", "audio")
        }),
        ("Business Information", {
            "classes": ("wide",),
            "fields": ("is_approved",)
        })
    )

    fieldsets = buffer_field_sets

    add_fieldsets = buffer_field_sets

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


admin.site.register(Multimedia, MultimediaAdmin)
