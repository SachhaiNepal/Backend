from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from branch.models import Member


class MemberAdmin(UserAdmin):
    list_display = (
        "name", "email", "address", "phone",
        "country", "district", "is_admin",
        "created_by", "approved_by"
    )
    list_filter = ("address", "is_active", "state")

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
            "fields": ("state", "is_active", "created_by", "updated_by", "approved_by")
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
            "fields": ("is_staff", "is_admin")
        })
    )

    search_fields = ("email", "name", "address", "country", "district")
    date_hierarchy = "created_at"
    ordering = (
        "name", "email", "address", "phone",
        "is_active", "state", "is_active",
        "created_by", "approved_by"
    )

    filter_horizontal = ()


admin.site.register(Member, MemberAdmin)
admin.site.unregister(Group)
