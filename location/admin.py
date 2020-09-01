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


admin.site.register(Country, CountryAdmin)
admin.site.register(Province, ProvinceAdmin)
admin.site.register(District, DistrictAdmin)
admin.site.register(Municipality)
admin.site.register(VDC)
admin.site.register(VDCWardNumber)
admin.site.register(MunicipalityWardNumber)
