import datetime
import time
import cookies
from bs4 import BeautifulSoup
from django.db import IntegrityError

from . import crawl
from ..models import liveNews


def krCrawl(lasttime):
    baseurl = "https://www.36kr.com"
    murl = "https://m.36kr.com"
    content = crawl(baseurl + "/newsflashes/catalog/0")
    soup = BeautifulSoup(content, "html.parser")
    for element in soup.find_all(name="a", attrs={"class": "item-title"}):
        try:
            newsrc = crawl(murl + element.get('href'))
            newssoup = BeautifulSoup(newsrc, "html.parser")
            pubtime = datetime.datetime.strptime(newssoup.find(attrs={"class": "newsflash-time"}).get_text(),
                                                 '%Y-%m-%d %H:%M')
            if pubtime <= lasttime:
                break
            news = liveNews()
            news.news_title = newssoup.find(attrs={"class": "newsflash-title"}).get_text()
            news.pub_time = newssoup.find(attrs={"class": "newsflash-time"}).get_text()
            news.news_content = newssoup.find(name="article").div.get_text()
            linktag = newssoup.find(attrs={"class": "origin-link"})
            if linktag:
                news.link = linktag.get('href')
            news.save()
        except IntegrityError as ie:
            print("资讯已存在")
            print(ie)
            continue
        except Exception as e:
            print(e)


def jmCrawl(lasttime):
    content = crawl("https://www.jiemian.com/lists/1325kb.html")
    soup = BeautifulSoup(content, "html.parser")
    for item in soup.find_all(attrs={"class": "columns-right-center__newsflash-item"}):
        try:
            pubtime = datetime.datetime.fromtimestamp(int(item.get('data-time')))
            if pubtime <= lasttime:
                break
            news = liveNews()
            news.pub_time = pubtime
            news.news_title = item.find(attrs={"class": "logStore"}).get_text()
            news.link = item.find(attrs={"class": "logStore"}).get('href')
            news.news_content = item.find(
                attrs={"class": "columns-right-center__newsflash-content__summary"}).get_text()
            news.save()
        except IntegrityError as ie:
            print("资讯已存在")
            print(ie)
            continue
        except Exception as e:
            print(e)


def lCrawl():
    lasttime = liveNews.objects.order_by('-pub_time')[0].pub_time.replace(tzinfo=None)
    krCrawl(lasttime)
    jmCrawl(lasttime)
