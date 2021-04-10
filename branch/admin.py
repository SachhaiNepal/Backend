from django.contrib import admin

from branch.models import Branch


class BranchAdmin(admin.ModelAdmin):
    list_display = (
        "name", "contact", "is_main",
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
        "name", "contact", "district__name", "is_main",
        "municipality__name", "municipality_ward__name",
        "vdc__name", "vdc_ward__name",
    )
    # list_filter = ()
    date_hierarchy = "created_at"
    fieldsets = (
        ("Branch Information", {
            "classes": ("wide", "extrapretty"),
            "fields" : (
                "name",
                "contact",
                "image",
                "is_main"
            )
        }),
        ("Location Information", {
            "classes": ("wide", "extrapretty"),
            "fields" : (
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
        "name", "contact", "is_main",
        "country", "province", "district",
        "municipality", "municipality_ward", "vdc", "vdc_ward",
        "created_by", "created_at", "updated_by", "updated_at"
    )

    list_per_page = 10

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        obj.image.delete()
        obj.delete()


admin.site.register(Branch, BranchAdmin)
