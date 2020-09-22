# -*- coding: utf-8 -*-
# Generated by Django 1.11.28 on 2020-08-19 19:42
from __future__ import unicode_literals

from django.db import migrations
import osf.utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('osf', '0214_auto_20200701_1658'),
    ]

    operations = [
        migrations.AddField(
            model_name='basefilenode',
            name='purged',
            field=osf.utils.fields.NonNaiveDateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='fileversion',
            name='purged',
            field=osf.utils.fields.NonNaiveDateTimeField(blank=True, null=True),
        ),
    ]