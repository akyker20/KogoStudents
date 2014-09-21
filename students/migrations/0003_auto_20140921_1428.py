# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0002_auto_20140921_1404'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='time',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='ridegroup',
            name='created_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
