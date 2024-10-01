from django.contrib import admin

from item_app.models import Item, Favorite, Tag


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['bdr_id', 'title', 'uri']


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['user', 'item', 'access']


admin.site.register(Tag)
