# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('UnifiedTest', '0012_auto_20150404_2306'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='response',
            field=models.TextField(blank=True),
        ),
    ]
