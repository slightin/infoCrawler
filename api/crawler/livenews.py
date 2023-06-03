import datetime
import time
import cookies
from bs4 import BeautifulSoup
from . import crawl
from ..models import liveNews

baseurl = "https://www.36kr.com"
murl = "https://m.36kr.com"
def lCrawl():
    lasttime=liveNews.objects.order_by('-pub_time')[0].pub_time.replace(tzinfo=None)
    content = crawl(baseurl + "/newsflashes/catalog/0")
    soup = BeautifulSoup(content, "html.parser")
    for element in soup.find_all(name="a", attrs={"class": "item-title"}):
        newsrc = crawl(murl + element.get('href'))
        newssoup = BeautifulSoup(newsrc, "html.parser")
        pubtime=datetime.datetime.strptime(newssoup.find(attrs={"class": "newsflash-time"}).get_text(),'%Y-%m-%d %H:%M')
        if pubtime<=lasttime:
            break
        news = liveNews()
        news.news_title = newssoup.find(attrs={"class": "newsflash-title"}).get_text()
        news.pub_time = newssoup.find(attrs={"class": "newsflash-time"}).get_text()
        news.news_content = newssoup.find(name="article").div.get_text()
        linktag = newssoup.find(attrs={"class": "origin-link"})
        if linktag:
            news.link = linktag.get('href')
        news.save()
