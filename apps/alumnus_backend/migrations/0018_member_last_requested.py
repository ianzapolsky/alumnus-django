# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('alumnus_backend', '0017_member_times_requested'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='last_requested',
            field=models.DateTimeField(default=django.utils.timezone.now, blank=True),
            preserve_default=False,
        ),
    ]
