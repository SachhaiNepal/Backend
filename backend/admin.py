from django.contrib import admin


class MyAdminSite(admin.AdminSite):
    site_header = "Sachhai Nepal Administration"
    site_title = "Sachhai Nepal Administration"
    index_title = "Administration Dashboard"
    enable_nav_sidebar = False
