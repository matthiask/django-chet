# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import easy_thumbnails.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='is active')),
                ('is_public', models.BooleanField(default=False, verbose_name='is public')),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now, verbose_name='created on')),
                ('date', models.DateField(default=django.utils.timezone.now, verbose_name='date')),
                ('title', models.CharField(max_length=200, verbose_name='title')),
                ('slug', models.SlugField(unique=True, max_length=200, verbose_name='slug')),
            ],
            options={
                'ordering': [b'-date'],
                'get_latest_by': b'date',
                'verbose_name': 'album',
                'verbose_name_plural': 'albums',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='is active')),
                ('is_public', models.BooleanField(default=False, verbose_name='is public')),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now, verbose_name='created on')),
                ('file', easy_thumbnails.fields.ThumbnailerImageField(upload_to=b'chet/photos/%Y/%m/', verbose_name='file')),
                ('shot_on', models.DateTimeField(default=django.utils.timezone.now, verbose_name='shot on')),
                ('title', models.CharField(max_length=200, verbose_name='title', blank=True)),
                ('is_dark', models.BooleanField(default=False, help_text='Dark images are shown on a light background.', verbose_name='is dark')),
                ('album', models.ForeignKey(verbose_name='album', to='chet.Album')),
            ],
            options={
                'ordering': [b'shot_on'],
                'get_latest_by': b'shot_on',
                'verbose_name': 'photo',
                'verbose_name_plural': 'photos',
            },
            bases=(models.Model,),
        ),
    ]
