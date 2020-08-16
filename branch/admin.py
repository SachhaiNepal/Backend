from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from branch.models import Member, Branch


class MemberAdmin(UserAdmin):
    list_display = (
        "name", "email", "address", "phone",
        "country", "district", "is_staff", "is_approved",
        "approved_by", "created_at", "updated_at"
    )
    list_filter = ("address", "is_active", "is_approved", "country", "district")

    fieldsets = (
        ("Authentication Information", {
            "classes": ("wide",),
            "fields": ("email", "password")
        }),
        ("Personal Information.", {
            "classes": ("wide",),
            "fields": ("name", "address", "phone", "country", "district")
        }),

        ("Business Details", {
            "classes": ("wide",),
            "fields": ("is_staff", "is_approved", "is_active", "approved_by")
        })
    )

    add_fieldsets = (
        ("Authentication Information", {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2"),
        }),
        ("Personal Information", {
            "classes": ("wide",),
            "fields": ("name", "address", "phone", "country", "district")
        }),
        ("Business Information", {
            "classes": ("wide",),
            "fields": ("is_staff",)
        })
    )

    search_fields = ("email", "name", "address", "country", "district")
    date_hierarchy = "created_at"
    ordering = (
        "name", "email", "address", "phone",
        "country", "district", "is_staff", "is_approved",
        "approved_by", "created_at", "updated_at"
    )

    filter_horizontal = ()


class BranchAdmin(admin.ModelAdmin):
    list_display = (
        "name", "address", "phone", "country", "district", "is_main",
        "created_by", "created_at", "updated_by", "updated_at"
    )

    fieldsets = (
        ("Branch Information", {
            "classes": ("wide",),
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


admin.site.register(Member, MemberAdmin)
admin.site.register(Branch, BranchAdmin)
admin.site.unregister(Group)
