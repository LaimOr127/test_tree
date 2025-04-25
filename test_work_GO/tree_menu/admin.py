from django.contrib import admin
from .models import Menu, MenuItem


class MenuItemInline(admin.TabularInline):
    model = MenuItem
    extra = 1
    fields = ('name', 'parent', 'url', 'named_url', 'order')
    raw_id_fields = ('parent',)


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('name',)
    inlines = [MenuItemInline]


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'menu', 'parent', 'url', 'named_url', 'order')
    list_filter = ('menu',)
    search_fields = ('name', 'url')
    raw_id_fields = ('parent',)
