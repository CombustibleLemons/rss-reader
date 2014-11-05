# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import main.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Feed',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('author', models.TextField()),
                ('category', models.TextField()),
                ('contributor', models.TextField()),
                ('description', models.TextField()),
                ('docURL', models.TextField()),
                ('editorAddr', models.TextField()),
                ('generator', models.TextField()),
                ('guid', models.TextField()),
                ('language', models.TextField()),
                ('logo', models.TextField()),
                ('rights', models.TextField()),
                ('subtitle', models.TextField()),
                ('title', models.TextField()),
                ('webmaster', models.TextField()),
                ('URL', models.URLField(unique=True)),
                ('ttl', models.IntegerField(null=True)),
                ('skipDays', models.IntegerField(null=True)),
                ('skipHours', models.IntegerField(null=True)),
                ('pubDate', models.DateTimeField(null=True)),
                ('updated', models.DateTimeField(null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('feedURL', models.TextField()),
                ('author', models.TextField()),
                ('category', main.models.ListField()),
                ('rights', models.TextField()),
                ('title', models.TextField()),
                ('subtitle', models.TextField()),
                ('content', models.TextField()),
                ('generator', models.TextField()),
                ('guid', models.TextField()),
                ('url', models.TextField()),
                ('contributor', models.TextField()),
                ('pubDate', models.DateTimeField(null=True)),
                ('updated', models.DateTimeField(null=True)),
                ('ackDate', models.FloatField(null=True)),
                ('feed', models.ForeignKey(to='main.Feed')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.TextField()),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
