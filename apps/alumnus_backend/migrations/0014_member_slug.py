# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alumnus_backend', '0013_auto_20150203_1547'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='slug',
            field=models.SlugField(default='hi', unique=True),
            preserve_default=False,
        ),
    ]
