# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-08 17:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0003_delete_userprofile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cpu',
            name='cpu_count',
        ),
        migrations.AddField(
            model_name='newassetapprovalzone',
            name='name',
            field=models.CharField(default='good', max_length=128, unique=True, verbose_name='\u8d44\u4ea7\u540d\u79f0'),
            preserve_default=False,
        ),
    ]
