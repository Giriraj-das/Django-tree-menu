from django.contrib import admin

from menu.models import Menu


class MenuAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'parent')


admin.site.register(Menu, MenuAdmin)
