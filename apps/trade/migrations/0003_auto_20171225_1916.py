# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-25 19:16
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0005_auto_20171205_1223'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('trade', '0002_auto_20171130_2209'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shoppingcart',
            old_name='good_num',
            new_name='nums',
        ),
        migrations.AlterUniqueTogether(
            name='shoppingcart',
            unique_together=set([('user', 'goods')]),
        ),
    ]
