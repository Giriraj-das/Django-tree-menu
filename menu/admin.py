from django.contrib import admin

from menu.models import Menu, MenuName


class MenuAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'parent', 'menu_name')


admin.site.register(Menu, MenuAdmin)
admin.site.register(MenuName)
