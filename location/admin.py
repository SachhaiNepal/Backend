from django.contrib import admin

from location.models import Country, Province, District, MunicipalityWard, Municipality, VDC, VDCWard


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
    ordering = ("name", "number", "country", "created_at", "updated_at")
    fieldsets = (
        ("Province Info", {
            "classes": ("wide", "extrapretty"),
            "fields": (
                "name", "number", "country"
            )
        }),
    )


class DistrictAdmin(admin.ModelAdmin):
    list_display = ("name", "province", "created_at", "updated_at")
    list_filter = ("province", "created_at", "updated_at")
    autocomplete_fields = ["province"]
    search_fields = (
        "name", "province__name", "province__country__name"
    )
    ordering = ("name", "province", "created_at", "updated_at")
    fieldsets = (
        ("District Info", {
            "classes": ("wide", "extrapretty"),
            "fields": (
                "name", "province"
            )
        }),
    )
    list_per_page = 10


class MunicipalityAdmin(admin.ModelAdmin):
    list_display = ("name", "district", "created_at", "updated_at")
    list_filter = ("created_at", "updated_at")
    autocomplete_fields = ["district"]
    search_fields = (
        "name",
        "district__name", "district__province__name", "district__province__country__name"
    )
    ordering = ("name", "district", "created_at", "updated_at")
    fieldsets = (
        ("Municipality Info", {
            "classes": ("wide", "extrapretty"),
            "fields": (
                "name", "district"
            )
        }),
    )
    list_per_page = 10


class MunicipalityWardAdmin(admin.ModelAdmin):
    list_display = ("name", "municipality", "number", "created_at", "updated_at")
    list_filter = ("created_at", "updated_at")
    autocomplete_fields = ["municipality"]
    search_fields = (
        "name", "number",
        "municipality__name", "municipality__district__name",
        "municipality__district__province__name", "municipality__district__province__country__name"
    )
    ordering = ("name", "municipality", "number", "created_at", "updated_at")
    fieldsets = (
        ("Municipality Ward Info", {
            "classes": ("wide", "extrapretty"),
            "fields": (
                "name", "municipality", "number"
            )
        }),
    )
    list_per_page = 10


class VDCAdmin(admin.ModelAdmin):
    list_display = ("name", "district", "created_at", "updated_at")
    list_filter = ("created_at", "updated_at")
    autocomplete_fields = ["district"]
    search_fields = (
        "name",
        "district__name", "district__province__name", "district__province__country__name"
    )
    ordering = ("name", "district", "created_at", "updated_at")
    fieldsets = (
        ("VDC Info", {
            "classes": ("wide", "extrapretty"),
            "fields": (
                "name", "district"
            )
        }),
    )
    list_per_page = 10


class VDCWardAdmin(admin.ModelAdmin):
    list_display = ("name", "vdc", "number", "created_at", "updated_at")
    list_filter = ("created_at", "updated_at")
    autocomplete_fields = ["vdc"]
    search_fields = (
        "name", "number",
        "vdc__name", "vdc__district__name", "vdc__district__province__name", "vdc__district__province__country__name"
    )
    ordering = ("name", "vdc", "number", "created_at", "updated_at")
    fieldsets = (
        ("District Info", {
            "classes": ("wide", "extrapretty"),
            "fields": (
                "name", "vdc", "number"
            )
        }),
    )
    list_per_page = 10


admin.site.register(Country, CountryAdmin)
admin.site.register(Province, ProvinceAdmin)
admin.site.register(District, DistrictAdmin)
admin.site.register(Municipality, MunicipalityAdmin)
admin.site.register(VDC, VDCAdmin)
admin.site.register(VDCWard, VDCWardAdmin)
admin.site.register(MunicipalityWard, MunicipalityWardAdmin)
