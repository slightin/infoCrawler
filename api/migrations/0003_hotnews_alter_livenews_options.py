# Generated by Django 4.1 on 2023-04-22 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_livenews_link_alter_livenews_pub_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='hotNews',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('link', models.CharField(default='', max_length=500)),
                ('rank', models.IntegerField()),
                ('hot', models.CharField(max_length=20)),
                ('src', models.CharField(max_length=20)),
            ],
        ),
        migrations.AlterModelOptions(
            name='livenews',
            options={'verbose_name': '实时资讯', 'verbose_name_plural': '实时资讯'},
        ),
    ]
