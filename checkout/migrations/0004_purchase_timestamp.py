# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0003_auto_20150324_2308'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 24, 23, 21, 56, 126430, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
