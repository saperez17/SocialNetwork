# Generated by Django 3.1.6 on 2021-02-28 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0013_auto_20210228_1431'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweet',
            name='datetime',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
