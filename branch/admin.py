from django.contrib import admin

from branch.models import Branch


class BranchAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "contact",
        "is_main",
        "country",
        "province",
        "district",
        "municipality",
        "municipality_ward",
        "vdc",
        "vdc_ward",
        "created_by",
        "updated_by",
        "timestamp",
    )
    autocomplete_fields = (
        "country",
        "province",
        "district",
        "municipality",
        "municipality_ward",
        "vdc",
        "vdc_ward",
    )
    search_fields = (
        "name",
        "contact",
        "district__name",
        "municipality__name",
        "municipality_ward__name",
        "vdc__name",
        "vdc_ward__name",
    )
    # list_filter = ()
    date_hierarchy = "created_at"
    fieldsets = (
        (
            "Branch Information",
            {
                "classes": ("wide", "extrapretty"),
                "fields": ("name", "contact"),
            },
        ),
        (
            "Location Information",
            {
                "classes": ("wide", "extrapretty"),
                "fields": (
                    "country",
                    "province",
                    "district",
                    "municipality",
                    "municipality_ward",
                    "vdc",
                    "vdc_ward",
                ),
            },
        ),
    )
    ordering = (
        "name",
        "contact",
        "is_main",
        "country",
        "province",
        "district",
        "municipality",
        "municipality_ward",
        "vdc",
        "vdc_ward",
        "created_by",
        "updated_by",
        "timestamp",
    )

    list_per_page = 10

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Branch, BranchAdmin)
