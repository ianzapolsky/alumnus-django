# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alumnus_backend', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MemberList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('members', models.ManyToManyField(to='alumnus_backend.Member')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
