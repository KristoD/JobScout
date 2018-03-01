# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-03-01 18:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employers', '0011_listing_charge_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConfirmListing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('company_description', models.TextField(blank=True)),
                ('job_description', models.TextField(blank=True)),
                ('city', models.CharField(max_length=45)),
                ('state', models.CharField(max_length=2)),
                ('employer', models.SmallIntegerField(null=True)),
            ],
        ),
    ]
