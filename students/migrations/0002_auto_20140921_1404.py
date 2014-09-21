# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RideGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField()),
                ('ending_loc', models.ForeignKey(related_name=b'dropoff_groups', to='students.Location')),
                ('starting_loc', models.ForeignKey(related_name=b'pickup_groups', to='students.Location')),
            ],
            options={
                'ordering': ['-created_at'],
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='request',
            name='group',
            field=models.ForeignKey(blank=True, to='students.RideGroup', null=True),
            preserve_default=True,
        ),
    ]
