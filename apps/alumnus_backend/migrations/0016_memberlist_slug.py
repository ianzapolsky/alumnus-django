# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alumnus_backend', '0015_organization_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='memberlist',
            name='slug',
            field=models.SlugField(default='memberlist-slug', unique=True),
            preserve_default=False,
        ),
    ]