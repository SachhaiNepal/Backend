from django.contrib import admin

from location.models import Country, Province, District, MunicipalityWardNumber, Municipality, VDC, VDCWardNumber


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


class MunicipalityAdmin(admin.ModelAdmin):
    list_display = ("name", "district", "created_at", "updated_at")
    list_filter = ("district", "created_at", "updated_at")
    autocomplete_fields = ["district"]
    search_fields = ("name",)
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


class MunicipalityWardNumberAdmin(admin.ModelAdmin):
    list_display = ("name", "municipality", "number", "created_at", "updated_at")
    list_filter = ("municipality", "number", "created_at", "updated_at")
    autocomplete_fields = ["municipality"]
    search_fields = ("name",)
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
    list_filter = ("district", "created_at", "updated_at")
    autocomplete_fields = ["district"]
    search_fields = ("name",)
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


class VDCWardNumberAdmin(admin.ModelAdmin):
    list_display = ("name", "vdc", "number", "created_at", "updated_at")
    list_filter = ("vdc", "number", "created_at", "updated_at")
    autocomplete_fields = ["vdc"]
    search_fields = ("name",)
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
admin.site.register(VDCWardNumber, VDCWardNumberAdmin)
admin.site.register(MunicipalityWardNumber, MunicipalityWardNumberAdmin)
