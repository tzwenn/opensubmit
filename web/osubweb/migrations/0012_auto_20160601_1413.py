# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-06-01 14:13


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('opensubmit', '0011_auto_20160413_1302'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='grading_notes',
            field=models.TextField(blank=True, help_text=b'Specific notes about the grading for this submission.', max_length=10000, null=True),
        ),
    ]