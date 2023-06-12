from django.db import models
import datetime
from django.utils import timezone


class liveNews(models.Model):
    news_title = models.CharField(max_length=200, unique=True, verbose_name="标题")
    pub_time = models.DateTimeField(default=timezone.now, verbose_name="发布日期")
    news_content = models.TextField(verbose_name="资讯内容")
    link = models.URLField(default='',verbose_name="原文链接")

    def __str__(self):
        return self.news_title

    class Meta:
        verbose_name = '实时资讯'
        verbose_name_plural = verbose_name


class hotNews(models.Model):
    title = models.CharField('内容', max_length=100)
    link = models.CharField('链接', max_length=500, default='')
    rank = models.IntegerField('排行榜')
    hot = models.CharField('热度', max_length=20)
    src = models.CharField('来源', max_length=20)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '聚合热搜'
        verbose_name_plural = verbose_name


class mainNews(models.Model):
    title = models.CharField('标题', max_length=100, unique=True)
    content = models.TextField('内容')
    imageurl = models.URLField('缩略图')
    pub_time = models.DateTimeField('发布时间', default=timezone.now)
    intro = models.TextField('简介', default='')
    bigimage = models.URLField('大图', default='')
    cate = models.ForeignKey('category', on_delete=models.DO_NOTHING, verbose_name="分类")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '主页资讯'
        verbose_name_plural = verbose_name


class category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
