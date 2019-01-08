# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-16 08:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instagram', '0010_auto_20170716_1307'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, default='default_avatar.png', height_field='height_field', upload_to='profile_image', width_field='width_field'),
        ),
    ]