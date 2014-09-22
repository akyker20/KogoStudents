# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('drivers', '0001_initial'),
        ('students', '0003_auto_20140921_1428'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ridegroup',
            options={'ordering': ['created_at']},
        ),
        migrations.AddField(
            model_name='ridegroup',
            name='driver',
            field=models.ForeignKey(blank=True, to='drivers.DriverProfile', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ridegroup',
            name='status',
            field=models.CharField(default=(b'w', b'Waiting'), max_length=8, choices=[(b'w', b'Waiting'), (b'r', b'Riding'), (b'c', b'Completed')]),
            preserve_default=True,
        ),
    ]
