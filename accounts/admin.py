from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.utils import timezone

from accounts.models import Member, ResetPasswordCode


class MemberInline(admin.StackedInline):
    model = Member
    extra = 0
    min_num = 0
    max_num = 1
    fk_name = "user"
    can_delete = False
    verbose_name_plural = "Add Branch Member Detail"

    exclude = ("approved_by", "approved_at")

    autocomplete_fields = ["branch", "country", "province", "district"]

    # update form for admin site
    fieldsets = (
        ("Personal Information", {
            "classes": ("wide", "extrapretty"),
            "fields" : ("image", "temporary_address", "permanent_address", "phone", "country", "province", "district",)
        }),
        ("Business Information", {
            "classes": ("wide", "extrapretty"),
            "fields" : ("branch", "is_approved")
        }),
    )


class UserAdmin(BaseUserAdmin):
    save_on_top = True
    inlines = (MemberInline,)

    list_display = (
        "username", "email", "first_name", "last_name",
        "is_superuser", "is_staff", "date_joined"
    )

    list_per_page = 10

    def save_formset(self, request, form, formset, change):
        if formset.model == Member:
            instances = formset.save(commit=False)
            print(instances)
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


class MemberAdmin(admin.ModelAdmin):
    list_display = (
        "user", "country", "province", "district", "phone",
        "branch", "is_approved", "approved_by", "approved_at",
    )
    list_filter = (
        ("is_approved", admin.BooleanFieldListFilter),
        ("branch__is_main", admin.BooleanFieldListFilter),
        ("approved_at", admin.DateFieldListFilter),

    )
    search_fields = (
        "user__username", "phone", "district__name",
        "branch__name", "district__name", "district__province__name",
        "district__province__country__name"
    )

    autocomplete_fields = ["branch", "country", "province", "district"]

    fieldsets = (
        ("Personal Information", {
            "classes": ("wide", "extrapretty"),
            "fields" : (
                "user", "phone", "image"
            )
        }),
        ("Location Information", {
            "classes": ("wide", "extrapretty"),
            "fields" : (
                "temporary_address", "permanent_address", "country", "province", "district"
            )
        }),
        ("Business Information", {
            "classes": ("wide", "extrapretty"),
            "fields" : (
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
        if change:
            this_record = Member.objects.get(pk=obj.pk)
            if this_record.is_approved and not obj.is_approved:
                obj.approved_by = None
                obj.approved_at = None
            if not this_record.is_approved and obj.is_approved:
                obj.approved_by = request.user
                obj.approved_at = timezone.now()
        else:
            if obj.is_approved:
                obj.approved_by = request.user
                obj.approved_at = timezone.now()
        super(MemberAdmin, self).save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        obj.image.delete()
        obj.delete()


class ResetPasswordCodeAdmin(admin.ModelAdmin):
    list_display = ("user", "code")
    list_per_page = 10


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Member, MemberAdmin)
admin.site.register(ResetPasswordCode, ResetPasswordCodeAdmin)
