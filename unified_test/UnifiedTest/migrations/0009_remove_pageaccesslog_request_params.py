# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('UnifiedTest', '0008_auto_20150404_1723'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pageaccesslog',
            name='request_params',
        ),
    ]
