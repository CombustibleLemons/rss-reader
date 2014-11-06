# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        ('main', '0003_auto_20141105_0828'),
    ]

    operations = [
        migrations.CreateModel(
            name='RSSUser',
            fields=[
                ('user_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            bases=('auth.user',),
        ),
        migrations.AlterField(
            model_name='topic',
            name='name',
            field=models.TextField(unique=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='topic',
            name='user',
            field=models.ForeignKey(to='main.RSSUser', null=True),
            preserve_default=True,
        ),
    ]
