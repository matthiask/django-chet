from __future__ import unicode_literals

from django import forms
from django.conf.urls import patterns, url
from django.contrib import admin
from django.contrib.admin.options import unquote  # util/utils really...
from django.contrib.admin.widgets import AdminFileWidget
from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpResponse
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.http import require_POST

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
    extra = 0

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'file':
            kwargs['widget'] = PhotoFileWidget
        return super(PhotoInline, self).formfield_for_dbfield(
            db_field, **kwargs)


class UploadForm(forms.Form):
    file = forms.FileField()


class AlbumAdmin(admin.ModelAdmin):
    date_hierarchy = 'date'
    inlines = [PhotoInline]
    list_display = ('title', 'date', 'is_active', 'is_public', 'photos')
    list_editable = ('is_active', 'is_public')
    list_filter = ('is_active', 'is_public')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title',)

    def get_urls(self):
        return patterns(
            '',
            url(
                r'^(?P<object_id>\d+)/upload/$',
                require_POST(self.admin_site.admin_view(self.upload)),
            ),
        ) + super(AlbumAdmin, self).get_urls()

    def upload(self, request, object_id):
        obj = self.get_object(request, unquote(object_id))

        if not self.has_change_permission(request, obj):
            raise PermissionDenied

        if obj is None:
            raise Http404

        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            photo = Photo(
                album=obj,
                file=form.cleaned_data['file'],
            )

            # TODO look into EXIF infos for determining `shot_on`
            if not photo.shot_on:
                photo.shot_on = obj.date

            photo.save()

        return HttpResponse('Thanks')


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
