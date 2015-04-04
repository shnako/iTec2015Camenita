# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('UnifiedTest', '0006_auto_20150404_1415'),
    ]

    operations = [
        migrations.CreateModel(
            name='PageAuthentication',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(default=b'Basic', max_length=10, choices=[(b'Basic', b'Basic'), (b'Headers', b'Headers'), (b'OAuth', b'OAuth')])),
                ('value', models.CharField(max_length=1024)),
            ],
        ),
        migrations.RemoveField(
            model_name='page',
            name='url',
        ),
        migrations.AddField(
            model_name='page',
            name='default_response',
            field=models.CharField(default=b'Static', max_length=50, choices=[(b'Static', b'Static'), (b'Dynamic', b'Dynamic')]),
        ),
        migrations.AddField(
            model_name='pageauthentication',
            name='page',
            field=models.ForeignKey(related_name='credentials', to='UnifiedTest.Page'),
        ),
    ]
