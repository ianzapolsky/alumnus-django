# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('alumnus_backend', '0011_auto_20150121_2117'),
    ]

    operations = [
        migrations.AddField(
            model_name='memberlist',
            name='uuid',
            field=models.CharField(default=uuid.uuid1, unique=True, max_length=100),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='organization',
            name='uuid',
            field=models.CharField(default=uuid.uuid1, unique=True, max_length=100),
            preserve_default=True,
        ),
    ]
