from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from accounts.models import Member


class MemberInline(admin.StackedInline):
    model = Member
    fk_name = "user"
    can_delete = False
    extra = 0
    verbose_name_plural = "Add Branch Member Detail"

    exclude = ("approved_by", "approved_at")

    # update form for admin site
    fieldsets = (
        ("Business Info", {
            "classes": ("wide", "extrapretty"),
            "fields": ("address", "phone", "country", "district", "branch", "is_approved")
        }),
    )


class UserAdmin(BaseUserAdmin):
    inlines = (MemberInline,)

    list_display = (
        "username", "email", "first_name", "last_name",
        "is_superuser", "is_staff", "date_joined"
    )

    def save_formset(self, request, form, formset, change):
        if formset.model == Member:
            instances = formset.save(commit=False)
            for instance in instances:
                if instance.is_approved:
                    instance.approved_by = request.user
                instance.save()
        else:
            formset.save()


class MemberAdmin(admin.ModelAdmin):
    list_display = (
        "user", "address", "country", "district", "phone",
        "branch", "is_approved", "approved_by", "approved_at",
    )
    list_filter = (
        ("is_approved", admin.BooleanFieldListFilter),
        ("branch", admin.RelatedFieldListFilter),
    )
    search_fields = ("user", "address", "phone")

    fieldsets = (
        ("Personal Info", {
            "classes": ("wide", "extrapretty"),
            "fields": (
                "user", "address", "phone", "country", "district"
            )
        }),
        ("Business Info", {
            "classes": ("wide", "extrapretty"),
            "fields": (
                "branch", "is_approved"
            )
        })
    )

    ordering = (
        "user", "address", "country", "district", "phone",
        "branch", "is_approved", "approved_by", "approved_at",
    )

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


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Member, MemberAdmin)
