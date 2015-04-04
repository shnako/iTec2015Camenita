# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('UnifiedTest', '0010_auto_20150404_1833'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='id',
            field=models.BigIntegerField(serialize=False, primary_key=True),
        ),
        migrations.AlterField(
            model_name='pageaccesslog',
            name='page',
            field=models.ForeignKey(related_name='access_logs', to='UnifiedTest.Page'),
        ),
        migrations.AlterField(
            model_name='pageaccesslog',
            name='request_method',
            field=models.CharField(max_length=20, choices=[(b'GET', b'GET'), (b'PUT', b'PUT'), (b'PATCH', b'PATCH'), (b'POST', b'POST'), (b'DELETE', b'DELETE'), (b'OPTIONS', b'OPTIONS'), (b'HEAD', b'HEAD')]),
        ),
        migrations.AlterField(
            model_name='pageauthentication',
            name='page',
            field=models.OneToOneField(related_name='authentication', to='UnifiedTest.Page'),
        ),
        migrations.AlterField(
            model_name='pageauthentication',
            name='type',
            field=models.CharField(default=b'None', max_length=10, choices=[(b'None', b'None'), (b'Basic', b'Basic'), (b'Headers', b'Headers'), (b'OAuth', b'OAuth')]),
        ),
        migrations.AlterField(
            model_name='pageauthentication',
            name='value',
            field=models.CharField(max_length=1024, blank=True),
        ),
    ]
