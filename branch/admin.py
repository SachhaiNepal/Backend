from django.contrib import admin

from branch.models import Branch


class BranchAdmin(admin.ModelAdmin):
    list_display = (
        "name", "phone", "is_main",
        "country", "province", "district",
        "municipality", "municipality_ward", "vdc", "vdc_ward",
        "created_by", "created_at", "updated_by", "updated_at"
    )
    autocomplete_fields = (
        "country", "province", "district",
        "municipality", "municipality_ward",
        "vdc", "vdc_ward",
    )
    search_fields = (
        "name", "phone", "district__name",
        "municipality__name", "municipality_ward__name",
        "vdc__name", "vdc_ward__name",
    )
    list_filter = (
        "is_main",
        "country",
        "province",
        "created_at",
    )
    date_hierarchy = "created_at"
    fieldsets = (
        ("Branch Information", {
            "classes": ("wide", "extrapretty"),
            "fields": (
                "name",
                "phone",
                "image",
                "is_main"
            )
        }),
        ("Location Information", {
            "classes": ("wide", "extrapretty"),
            "fields": (
                "country",
                "province",
                "district",
                "municipality",
                "municipality_ward",
                "vdc",
                "vdc_ward"
            )
        })
    )
    ordering = (
        "name", "phone", "is_main",
        "country", "province", "district",
        "municipality", "municipality_ward", "vdc", "vdc_ward",
        "created_by", "created_at", "updated_by", "updated_at"
    )

    list_per_page = 10

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
