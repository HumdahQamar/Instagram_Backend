# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-14 13:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instagram', '0002_auto_20170714_1239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='instagram/avatars/', verbose_name='Avatar'),
        ),
    ]