from django.contrib import admin

from chet.models import Album, Photo


class AlbumAdmin(admin.ModelAdmin):
    date_hierarchy = 'date'
    list_display = ('title', 'date', 'is_active', 'is_public')
    list_editable = ('is_active', 'is_public')
    list_filter = ('is_active', 'is_public')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title',)


class PhotoAdmin(admin.ModelAdmin):
    date_hierarchy = 'shot_on'
    # TODO add thumb
    list_display = (
        '__unicode__', 'shot_on', 'is_active', 'is_public', 'is_dark')
    list_editable = ('is_active', 'is_public', 'is_dark')
    list_filter = ('is_active', 'is_public', 'is_dark', 'album')
    search_fields = ('title',)


admin.site.register(Album, AlbumAdmin)
admin.site.register(Photo, PhotoAdmin)
