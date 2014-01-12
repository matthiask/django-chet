from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.admin.widgets import AdminFileWidget
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from easy_thumbnails.files import get_thumbnailer

from chet.models import Album, Photo


class PhotoFileWidget(AdminFileWidget):
    thumb_template = (
        '<img src="{0}" alt="" style="float:left;margin-right:10px">')

    def render(self, name, value, attrs=None):
        html = super(PhotoFileWidget, self).render(name, value, attrs)

        if value is None:
            return html

        options = {'size': (100, 100), 'crop': True}
        thumb_url = get_thumbnailer(value).get_thumbnail(options).url
        thumb = self.thumb_template.format(thumb_url)

        return mark_safe('{0} {1}'.format(thumb, html))


class PhotoInline(admin.TabularInline):
    model = Photo
    fields = ('file', 'title', 'shot_on', 'is_active', 'is_public', 'is_dark')

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'file':
            kwargs['widget'] = PhotoFileWidget
        return super(PhotoInline, self).formfield_for_dbfield(
            db_field, **kwargs)


class AlbumAdmin(admin.ModelAdmin):
    date_hierarchy = 'date'
    inlines = [PhotoInline]
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

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'file':
            kwargs['widget'] = PhotoFileWidget
        return super(PhotoAdmin, self).formfield_for_dbfield(
            db_field, **kwargs)

    def thumbnail(self, photo):
        options = {'size': (100, 100), 'crop': True}
        thumb_url = get_thumbnailer(photo.file).get_thumbnail(options).url
        return '<img src="{0}" alt="">'.format(thumb_url)

    thumbnail.allow_tags = True
    thumbnail.short_description = 'thumb'


admin.site.register(Album, AlbumAdmin)
admin.site.register(Photo, PhotoAdmin)
