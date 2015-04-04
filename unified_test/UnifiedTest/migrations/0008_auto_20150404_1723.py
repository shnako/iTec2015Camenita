# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('UnifiedTest', '0007_auto_20150404_1704'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pageaccesslog',
            old_name='request_type',
            new_name='request_method',
        ),
        migrations.AddField(
            model_name='pageaccesslog',
            name='request_params',
            field=models.CharField(max_length=2000, blank=True),
        ),
    ]
