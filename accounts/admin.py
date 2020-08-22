from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from accounts.models import Member


class MemberAdmin(UserAdmin):
    list_display = (
        "name", "branch",
        "district", "is_staff", "is_approved",
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
            "fields": ("branch", "is_staff", "is_approved", "is_active")
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
        "name", "branch",
        "district", "is_staff", "is_approved",
        "approved_by", "created_at", "updated_at"
    )

    filter_horizontal = ()

    def save_model(self, request, obj, form, change):
        if obj.is_approved:
            obj.approved_by = request.user
        obj.save()

    def save_formset(self, request, form, formset, change):
        if formset.model == Member:
            instances = formset.save(commit=False)
            for instance in instances:
                if instance.is_approved:
                    instance.approved_by = request.user
                instance.save()
        else:
            formset.save()


admin.site.register(Member, MemberAdmin)
admin.site.unregister(Group)
