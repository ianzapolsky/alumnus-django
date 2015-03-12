# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alumnus_backend', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='participant_type',
            field=models.CharField(blank=True, max_length=100, choices=[(b'Current', b'Current Member'), (b'Past', b'Past Member'), (b'Friend/Family', b'Friend/Family of Member')]),
            preserve_default=True,
        ),
    ]
