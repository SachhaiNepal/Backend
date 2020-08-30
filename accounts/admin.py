from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.utils import timezone

from accounts.models import Member, Country, Province, District, ResetPasswordCode


class MemberInline(admin.StackedInline):
    model = Member
    fk_name = "user"
    can_delete = False
    extra = 1
    verbose_name_plural = "Add Branch Member Detail"

    exclude = ("approved_by", "approved_at")

    autocomplete_fields = ["branch", "country", "province", "district"]

    # update form for admin site
    fieldsets = (
        ("Personal Info", {
            "classes": ("wide", "extrapretty"),
            "fields": ("temporary_address", "permanent_address", "phone", "country", "province", "district",)
        }),
        ("Business Info", {
            "classes": ("wide", "extrapretty"),
            "fields": ("branch", "is_approved")
        }),
    )


def save_form_set(self, request, form, formset, change):
    if formset.model == Member:
        instances = formset.save(commit=False)
        for instance in instances:
            if instance.is_approved:
                instance.approved_by = request.user
                instance.approved_at = timezone.now()
            instance.save()
    else:
        formset.save()


class UserAdmin(BaseUserAdmin):
    inlines = (MemberInline,)

    list_display = (
        "username", "email", "first_name", "last_name",
        "is_superuser", "is_staff", "date_joined"
    )

    list_per_page = 10

    def save_formset(self, request, form, formset, change):
        save_form_set(self, request, form, formset, change)


class MemberAdmin(admin.ModelAdmin):
    list_display = (
        "user", "country", "province", "district", "phone",
        "branch", "is_approved", "approved_by", "approved_at",
    )
    list_filter = (
        ("is_approved", admin.BooleanFieldListFilter),
        ("branch", admin.RelatedFieldListFilter),
        ("approved_at", admin.DateFieldListFilter),
        ("province", admin.RelatedFieldListFilter),
        ("country", admin.RelatedFieldListFilter)
    )
    search_fields = ("user__username", "phone", "district__name")

    autocomplete_fields = ["branch", "country", "province", "district"]

    fieldsets = (
        ("Personal Info", {
            "classes": ("wide", "extrapretty"),
            "fields": (
                "user", "temporary_address", "permanent_address", "phone", "country", "province", "district"
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
        "user", "country", "province", "district", "phone",
        "branch", "is_approved", "approved_by", "approved_at",
    )

    list_per_page = 10

    def save_model(self, request, obj, form, change):
        if obj.is_approved:
            obj.approved_by = request.user
            obj.approved_at = timezone.now()
        obj.save()

    def save_formset(self, request, form, formset, change):
        save_form_set(self, request, form, formset, change)


class CountryAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at", "updated_at")
    list_filter = ("created_at", "updated_at")
    search_fields = ("name",)
    ordering = ("name", "created_at", "updated_at")
    fieldsets = (
        ("Country Info", {
            "classes": ("wide", "extrapretty"),
            "fields": (
                "name",
            )
        }),
    )


class ProvinceAdmin(admin.ModelAdmin):
    list_display = ("name", "number", "country", "created_at", "updated_at")
    list_filter = ("country", "created_at", "updated_at")
    autocomplete_fields = ["country"]
    search_fields = ("name",)
    ordering = ("name", "country", "country", "created_at", "updated_at")
    fieldsets = (
        ("District Info", {
            "classes": ("wide", "extrapretty"),
            "fields": (
                "name", "number", "country"
            )
        }),
    )


class DistrictAdmin(admin.ModelAdmin):
    list_display = ("name", "country", "province", "created_at", "updated_at")
    list_filter = ("country", "province", "created_at", "updated_at")
    autocomplete_fields = ["country", "province"]
    search_fields = ("name",)
    ordering = ("name", "country", "province", "created_at", "updated_at")
    fieldsets = (
        ("District Info", {
            "classes": ("wide", "extrapretty"),
            "fields": (
                "name", "country", "province"
            )
        }),
    )
    list_per_page = 10


class ResetPasswordCodeAdmin(admin.ModelAdmin):
    list_display = ("user", "code")
    list_per_page = 10


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Member, MemberAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(Province, ProvinceAdmin)
admin.site.register(District, DistrictAdmin)
admin.site.register(ResetPasswordCode, ResetPasswordCodeAdmin)
