# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FilterResult',
            fields=[
                ('filter_name', models.TextField(primary_key=True)),
                ('date', models.TextField(serialize=False, primary_key=True)),
                ('contract', models.TextField(primary_key=True)),
            ],
            options={
                'db_table': 'filter_result',
                'managed': False,
            },
        ),
    ]
