# Generated by Django 4.1 on 2023-04-11 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='liveNews',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('news_title', models.CharField(max_length=200)),
                ('pub_time', models.DateTimeField(default=None, verbose_name='date published')),
                ('news_content', models.CharField(max_length=500)),
                ('link', models.CharField(default=None, max_length=50)),
            ],
        ),
    ]
