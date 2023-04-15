from django.contrib import admin
from django.db import models
import datetime
from django.utils import timezone


class liveNews(models.Model):
    news_title = models.CharField(max_length=200)
    pub_time = models.DateTimeField('date published', default=timezone.now)
    news_content = models.CharField(max_length=500)
    link = models.CharField(max_length=200, default='')

    # @admin.display(
    #     boolean=True,
    #     ordering='pub_time',
    # )

    def __str__(self):
        return self.news_title

    class Meta:
        # db_table = ''
        # managed = True
        verbose_name = '实时资讯'
        verbose_name_plural = verbose_name
