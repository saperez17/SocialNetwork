# Generated by Django 3.1.6 on 2021-02-27 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_auto_20210227_1104'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweet',
            name='likes',
            field=models.IntegerField(default=0),
        ),
    ]
