# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alumnus_backend', '0008_member_gender'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='company',
            field=models.CharField(max_length=100, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='member',
            name='graduation_year',
            field=models.CharField(blank=True, max_length=4, choices=[(b'1990', b'1990'), (b'1991', b'1991'), (b'1992', b'1992'), (b'1993', b'1993'), (b'1994', b'1994'), (b'1995', b'1995'), (b'1996', b'1996'), (b'1997', b'1997'), (b'1998', b'1998'), (b'1999', b'1999'), (b'2000', b'2000'), (b'2001', b'2001'), (b'2002', b'2002'), (b'2003', b'2003'), (b'2004', b'2004'), (b'2005', b'2005'), (b'2006', b'2006'), (b'2007', b'2007'), (b'2008', b'2008'), (b'2009', b'2009'), (b'2010', b'2010'), (b'2011', b'2011'), (b'2012', b'2012'), (b'2013', b'2013'), (b'2014', b'2014'), (b'2015', b'2015'), (b'2016', b'2016'), (b'2017', b'2017'), (b'2018', b'2018'), (b'2019', b'2019'), (b'2020', b'2020'), (b'2021', b'2021')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='member',
            name='industry',
            field=models.CharField(max_length=100, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='member',
            name='school',
            field=models.CharField(blank=True, max_length=10, choices=[(b'CC', b'CC'), (b'SEAS', b'SEAS'), (b'GS', b'GS'), (b'BC', b'BC')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='member',
            name='gender',
            field=models.CharField(blank=True, max_length=10, choices=[(b'Male', b'Male'), (b'Female', b'Female')]),
            preserve_default=True,
        ),
    ]
