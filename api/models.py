from django.contrib import admin
from django.db import models
import datetime
from django.utils import timezone


class liveNews(models.Model):
    news_title = models.CharField(max_length=200, unique=True)
    pub_time = models.DateTimeField('date published', default=timezone.now)
    news_content = models.TextField()
    link = models.CharField(max_length=200, default='')

    def __str__(self):
        return self.news_title

    class Meta:
        verbose_name = '实时资讯'
        verbose_name_plural = verbose_name


class hotNews(models.Model):
    title = models.CharField(max_length=100)
    link = models.CharField(max_length=500, default='')
    rank = models.IntegerField()
    hot = models.CharField(max_length=20)
    src = models.CharField(max_length=20)


class mainNews(models.Model):
    title = models.CharField(max_length=100, unique=True)
    content = models.TextField()
    imageurl = models.URLField()
    pub_time = models.DateTimeField(default=timezone.now)
    intro = models.TextField(default='')
    bigimage = models.URLField(default='')
    cate = models.ForeignKey('category', on_delete=models.DO_NOTHING)


class category(models.Model):
    name = models.CharField(max_length=50, unique=True)
