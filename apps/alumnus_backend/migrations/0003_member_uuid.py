# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('alumnus_backend', '0002_memberlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='uuid',
            field=models.CharField(default=uuid.uuid4, unique=True, max_length=100),
            preserve_default=True,
        ),
    ]
