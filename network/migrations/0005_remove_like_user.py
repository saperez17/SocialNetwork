# Generated by Django 3.1.6 on 2021-02-27 22:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0004_like'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='like',
            name='user',
        ),
    ]
