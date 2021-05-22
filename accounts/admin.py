from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.utils import timezone

from accounts.models import *


class ProfileAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = (
        "user",
        "bio",
        "contact",
        "birth_date",
        "current_city",
        "home_town",
        "country",
        "province",
        "district",
        "last_updated",
    )
    ordering = (
        "user",
        "bio",
        "contact",
        "birth_date",
        "current_city",
        "home_town",
        "country",
        "province",
        "district",
        "last_updated",
    )
    list_filter = (
        ("country", admin.RelatedFieldListFilter),
        ("province", admin.RelatedFieldListFilter),
        ("district", admin.RelatedFieldListFilter),
        ("last_updated", admin.DateFieldListFilter),
    )
    search_fields = (
        "user__username",
        "contact",
        "district__name",
        "district__name",
        "district__province__name",
        "district__province__country__name",
    )
    autocomplete_fields = ["country", "province", "district"]

    fieldsets = (
        (
            "Personal Information",
            {
                "classes": ("wide", "extrapretty"),
                "fields": ("contact", "bio", "birth_date"),
            },
        ),
        (
            "Location Information",
            {
                "classes": ("wide", "extrapretty"),
                "fields": (
                    "current_city",
                    "home_town",
                    "country",
                    "province",
                    "district",
                ),
            },
        ),
    )
    list_per_page = 10


class UserAdmin(BaseUserAdmin):
    save_on_top = True
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_superuser",
        "is_staff",
        "date_joined",
    )

    list_per_page = 10

    def save_formset(self, request, form, formset, change):
        if formset.model == Member:
            instances = formset.save(commit=False)
            for instance in instances:
                if change:
                    this_record = Member.objects.get(pk=instance.pk)
                    if this_record.is_approved and not instance.is_approved:
                        instance.approved_by = None
                        instance.approved_at = None
                    if not this_record.is_approved and instance.is_approved:
                        instance.approved_by = request.user
                        instance.approved_at = timezone.now()
                else:
                    if instance.is_approved:
                        instance.approved_by = request.user
                        instance.approved_at = timezone.now()
                instance.save()
        else:
            formset.save()


class MemberBranchInline(admin.StackedInline):
    model = MemberBranch
    extra = 0
    min_num = 1
    max_num = 1
    fk_name = "member"
    can_delete = True
    verbose_name_plural = "Add Branch Detail"

    # update form for admin site
    fieldsets = (
        (
            "Business Information",
            {
                "classes": ("wide", "extrapretty"),
                "fields": ("branch", "date_of_membership"),
            },
        ),
    )


class MemberRoleInline(admin.StackedInline):
    model = MemberRole
    extra = 0
    min_num = 1
    max_num = 10
    fk_name = "member"
    can_delete = True
    verbose_name_plural = "Add Branch Role Detail"

    # update form for admin site
    fieldsets = (
        (
            "Business Information",
            {
                "classes": ("wide", "extrapretty"),
                "fields": (
                    "role_name",
                    "from_date",
                    "to_date",
                    "member_branch",
                ),
            },
        ),
    )


class MemberRoleAdmin(admin.ModelAdmin):
    list_display = (
        "member",
        "member_branch",
        "role_name",
        "from_date",
        "to_date",
    )
    ordering = (
        "member",
        "member_branch",
        "role_name",
        "from_date",
        "to_date",
    )

    list_per_page = 10
    list_filter = ("member", "from_date", "to_date")
    search_fields = ("member__user__username", "member__user__email")

    autocomplete_fields = ["member"]


class MemberBranchAdmin(admin.ModelAdmin):
    list_display = ("member", "branch", "date_of_membership")
    ordering = ("member", "branch", "date_of_membership")

    list_per_page = 10
    list_filter = ("member", "date_of_membership")
    search_fields = ("member__user__username", "member__user__email")

    autocomplete_fields = ["member", "branch"]


class MemberAdmin(admin.ModelAdmin):
    save_on_top = True
    inlines = (MemberBranchInline, MemberRoleInline)

    list_display = (
        "user",
        "is_approved",
        "approved_by",
        "approved_at",
    )
    list_filter = (
        ("is_approved", admin.BooleanFieldListFilter),
        ("approved_at", admin.DateFieldListFilter),
    )
    search_fields = (
        "user__username",
        "district__name",
        "district__name",
        "district__province__name",
        "district__province__country__name",
    )
    fieldsets = (
        (
            "Select Follower",
            {
                "classes": ("wide", "extrapretty"),
                "fields": ("user",),
            },
        ),
    )

    ordering = (
        "user",
        "is_approved",
        "approved_by",
        "approved_at",
    )

    list_per_page = 10

    def save_model(self, request, obj, form, change):
        if change:
            obj.updated_by = request.user
        else:
            obj.created_by = request.user
        super(MemberAdmin, self).save_model(request, obj, form, change)


class ResetPasswordCodeAdmin(admin.ModelAdmin):
    list_display = ("user", "code")
    list_per_page = 10


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Member, MemberAdmin)
admin.site.register(MemberRole, MemberRoleAdmin)
admin.site.register(MemberBranch, MemberBranchAdmin)
admin.site.register(ResetPasswordCode, ResetPasswordCodeAdmin)
