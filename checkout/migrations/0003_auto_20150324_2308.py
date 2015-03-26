# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0002_purchase'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchase',
            name='products',
        ),
        migrations.AddField(
            model_name='purchase',
            name='items_list',
            field=models.CharField(default=0, max_length=200),
            preserve_default=False,
        ),
    ]
