from django.contrib import admin

from branch.models import Branch


class BranchAdmin(admin.ModelAdmin):
    list_display = (
        "name", "address", "phone", "country", "district", "is_main",
        "created_by", "created_at", "updated_by", "updated_at"
    )

    fieldsets = (
        ("Branch Information", {
            "classes": ("wide", "extrapretty"),
            "fields": ("name", "address", "phone", "country", "district", "is_main")
        }),
    )

    search_fields = ("name", "address", "phone", "district")
    list_filter = ("is_main", "country")
    date_hierarchy = "created_at"
    ordering = ("name", "address", "phone", "country", "district", "is_main")

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        obj.updated_by = request.user
        obj.save()

    def save_formset(self, request, form, formset, change):
        if formset.model == Branch:
            instances = formset.save(commit=False)
            for instance in instances:
                instance.updated_by = request.user
                instance.save()
        else:
            formset.save()


admin.site.register(Branch, BranchAdmin)
