# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alumnus_backend', '0016_memberlist_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='times_requested',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
