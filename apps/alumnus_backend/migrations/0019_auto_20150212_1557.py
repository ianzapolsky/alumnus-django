# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alumnus_backend', '0018_member_last_requested'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='last_requested',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
