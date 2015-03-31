# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('alumnus_backend', '0002_member_participant_type'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='member',
            options={'ordering': ['lastname', 'firstname']},
        ),
        migrations.AlterModelOptions(
            name='memberlist',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='organization',
            options={'ordering': ['name']},
        ),
        migrations.AddField(
            model_name='organization',
            name='privileged_users',
            field=models.ManyToManyField(related_name='privileged_users', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
