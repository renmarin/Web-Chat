# Generated by Django 3.2.9 on 2021-11-25 00:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_chat', '0003_alter_chat_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 25, 2, 29, 40, 358923)),
        ),
    ]
