# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-21 08:10
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('instagram', '0017_auto_20170721_1127'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Followers',
            new_name='Follow_Information',
        ),
    ]
