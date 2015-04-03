# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status_code', models.PositiveIntegerField(default=200)),
                ('delay', models.PositiveIntegerField(default=0, null=True, blank=True)),
                ('response', models.TextField()),
                ('dynamic_code', models.TextField()),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PageAccessLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField()),
                ('request_type', models.CharField(max_length=20, choices=[(b'get', b'GET'), (b'put', b'PUT'), (b'post', b'POST'), (b'delete', b'DELETE'), (b'options', b'OPTIONS'), (b'head', b'HEAD')])),
                ('request_body', models.TextField()),
                ('response_body', models.TextField()),
                ('page', models.ForeignKey(to='UnifiedTest.Page')),
            ],
        ),
    ]
