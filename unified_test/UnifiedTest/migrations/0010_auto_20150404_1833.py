# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('UnifiedTest', '0009_remove_pageaccesslog_request_params'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pageaccesslog',
            name='response_body',
            field=models.TextField(blank=True),
        ),
    ]
