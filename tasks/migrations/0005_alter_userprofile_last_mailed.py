# Generated by Django 4.0.1 on 2022-02-23 23:14

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0004_userprofile_last_mailed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='last_mailed',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 2, 23, 23, 14, 3, 983038, tzinfo=utc), null=True),
        ),
    ]
