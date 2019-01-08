# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-14 18:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instagram', '0003_auto_20170714_1811'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, default='instagram/avatars/default_avatar.png', upload_to='instagram/static/instagram/avatars/', verbose_name='Avatar'),
        ),
    ]