from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from easy_thumbnails.files import get_thumbnailer

from chet.models import Album, Photo


class AlbumAdmin(admin.ModelAdmin):
    date_hierarchy = 'date'
    list_display = ('title', 'date', 'is_active', 'is_public', 'photos')
    list_editable = ('is_active', 'is_public')
    list_filter = ('is_active', 'is_public')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title',)

    def photos(self, instance):
        return instance.photos.count()
    photos.short_description = _('photos')


class PhotoAdmin(admin.ModelAdmin):
    date_hierarchy = 'shot_on'
    list_display = (
        'thumbnail', 'title', 'shot_on', 'is_active', 'is_public', 'is_dark')
    list_editable = ('title', 'shot_on', 'is_active', 'is_public', 'is_dark')
    list_filter = ('is_active', 'is_public', 'is_dark', 'album')
    search_fields = ('title',)

    def thumbnail(self, photo):
        options = {'size': (100, 100), 'crop': True}
        thumb_url = get_thumbnailer(photo.file).get_thumbnail(options).url
        return '<img src="{0}" alt="">'.format(thumb_url)

    thumbnail.allow_tags = True
    thumbnail.short_description = 'thumb'


admin.site.register(Album, AlbumAdmin)
admin.site.register(Photo, PhotoAdmin)
