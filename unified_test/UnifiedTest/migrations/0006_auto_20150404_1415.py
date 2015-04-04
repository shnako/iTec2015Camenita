# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('UnifiedTest', '0005_auto_20150403_1820'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='ref',
            field=models.CharField(default='', unique=True, max_length=64),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='pageaccesslog',
            name='request_type',
            field=models.CharField(max_length=20, choices=[(b'GET', b'GET'), (b'PUT', b'PUT'), (b'POST', b'POST'), (b'DELETE', b'DELETE'), (b'OPTIONS', b'OPTIONS'), (b'HEAD', b'HEAD')]),
        ),
    ]
