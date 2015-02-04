# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alumnus_backend', '0014_member_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='slug',
            field=models.SlugField(default='organization-slug', unique=True),
            preserve_default=False,
        ),
    ]
