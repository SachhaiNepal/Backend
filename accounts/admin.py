from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from accounts.models import Member


class MemberAdmin(UserAdmin):
    list_display = (
        "name", "branch", "email", "address", "phone",
        "country", "district", "is_staff", "is_approved",
        "approved_by", "created_at", "updated_at"
    )
    list_filter = ("address", "is_active", "is_approved", "country", "branch")

    # update form for admin site
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
            "fields": ("branch", "is_staff", "is_approved", "is_active", "approved_by")
        })
    )

    # create form for admin site
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
            "fields": ("branch", "is_staff",)
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


admin.site.register(Member, MemberAdmin)
admin.site.unregister(Group)
