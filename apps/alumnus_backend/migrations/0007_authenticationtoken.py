# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('alumnus_backend', '0006_member_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuthenticationToken',
            fields=[
                ('accesstoken_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='alumnus_backend.AccessToken')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=('alumnus_backend.accesstoken',),
        ),
    ]
