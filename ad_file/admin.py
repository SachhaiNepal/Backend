from django.contrib import admin

from ad_file.models import AdFile



class AdFileAdmin(admin.ModelAdmin):
    list_display = ("name","phone"
        
    )

    search_fields = ("name", "phone"
        
    )
    list_filter = ("name", "phone"
        
    )
   # date_hierarchy = "created_at"
    fieldsets = (
        (" AdFileInformation", {
            "classes": ("wide", "extrapretty"),
            "fields": (
                "name",
                "phone",
                "image"
            )
        }),
       
    )
    ordering = (
        "name", "phone"
        
    )

    list_per_page = 10

    


admin.site.register(AdFile,AdFileAdmin)







