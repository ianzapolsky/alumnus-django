# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alumnus_backend', '0003_member_uuid'),
    ]

    operations = [
        migrations.AddField(
            model_name='memberlist',
            name='organization',
            field=models.ForeignKey(default=1, to='alumnus_backend.Organization'),
            preserve_default=False,
        ),
    ]
