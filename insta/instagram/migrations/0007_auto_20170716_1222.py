# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-16 07:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instagram', '0006_auto_20170716_1216'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, upload_to='profile_image'),
        ),
    ]