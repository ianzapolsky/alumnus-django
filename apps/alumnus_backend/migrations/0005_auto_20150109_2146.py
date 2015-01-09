# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('alumnus_backend', '0004_memberlist_organization'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccessToken',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('token', models.CharField(default=uuid.uuid1, unique=True, max_length=255)),
                ('used', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='member',
            name='uuid',
            field=models.CharField(default=uuid.uuid1, unique=True, max_length=100),
            preserve_default=True,
        ),
    ]
