# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alumnus_backend', '0007_authenticationtoken'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='gender',
            field=models.CharField(default='Male', max_length=10, choices=[(b'Male', b'Male'), (b'Female', b'Female')]),
            preserve_default=False,
        ),
    ]
