# Generated by Django 3.1.6 on 2021-02-27 22:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0003_tweet_likes'),
    ]

    operations = [
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tweet', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='likes_tweet', to='network.tweet')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes_users', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
