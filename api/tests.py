import re
import time
import datetime
from bs4 import BeautifulSoup
import json
from django.core import serializers
from django.http import JsonResponse
from django.test import TestCase
from .crawler import crawl, driver_path
from .crawler.livenews import baseurl, murl
from .models import liveNews
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CrawlerTests(TestCase):
    def testlivenews_pc(self):
        content = crawl(baseurl + "/newsflashes/catalog/0")
        soup = BeautifulSoup(content, "html.parser")
        for element in soup.find_all(name="a", attrs={"class": "item-title"}):
            # element=soup.find_all(name="a", attrs={"class": "item-title"})[0]
            newsrc = crawl(baseurl + element.get('href'))
            newssoup = BeautifulSoup(newsrc, "html.parser")
            news = liveNews()
            news.news_title = newssoup.find(attrs={"class": "item-title"}).get_text()
            news.pubtime = time.strptime(newssoup.find(attrs={"class": "time"}).get_text(), '%Y-%m-%d %H:%M')
            news.news_content = newssoup.find(attrs={"class": "pre-item-des"}).get_text()
            linktag = newssoup.find(attrs={"class": "article-link-icon"})
            if linktag:
                news.link = linktag.get('href')
            # print(news.news_title+news.news_content)
            news.save()

    def testlivenews_m(self):
        lasttime = liveNews.objects.order_by('-pub_time')[0].pub_time.replace(tzinfo=None)
        content = crawl(baseurl + "/newsflashes/catalog/0")
        soup = BeautifulSoup(content, "html.parser")
        for element in soup.find_all(name="a", attrs={"class": "item-title"}):
            # element=soup.find_all(name="a", attrs={"class": "item-title"})[0]
            newsrc = crawl(murl + element.get('href'))
            newssoup = BeautifulSoup(newsrc, "html.parser")
            pubtime = datetime.datetime.strptime(newssoup.find(attrs={"class": "newsflash-time"}).get_text(),
                                                 '%Y-%m-%d %H:%M')
            if pubtime <= lasttime:
                break
            print(newssoup.find(attrs={"class": "newsflash-time"}).get_text())
            # news = liveNews()
            # news.news_title = newssoup.find(attrs={"class": "newsflash-title"}).get_text()
            # news.pubtime = newssoup.find(attrs={"class": "newsflash-time"}).get_text()
            # news.news_content = newssoup.find(name="article").get_text()
            # linktag = newssoup.find(attrs={"class": "origin-link"})
            # if linktag:
            #     news.link = linktag.get('href')
            # # print(news.news_title+news.news_content)
            # news.save()

    def testlinktime(self):
        content = crawl("https://m.36kr.com/newsflashes/2214987967821185")
        soup = BeautifulSoup(content, "html.parser")
        print(soup.find(attrs={"class": "newsflash-title"}).get_text())
        print(soup.find(name="article").div.get_text())
        # print(time.strptime(soup.find(attrs={"class": "newsflash-time"}).get_text(), '%Y-%m-%d %H:%M'))
        print(soup.find(attrs={"class": "newsflash-time"}).get_text())
        print(soup.find(attrs={"class": "origin-link"}).get('href'))
        # linktag = soup.find(attrs={"class": "article-link-icon"})
        # print(soup.find(attrs={"class": "article-link-icon"}).get_text())
        # if linktag:
        #     print(linktag.get('href'))

    def testselenium(self):
        driver=webdriver.Edge(driver_path)
        driver.implicitly_wait(10)
        driver.get('https://s.weibo.com/top/summary?cate=realtimehot')
        hotlist=driver.find_elements(By.CSS_SELECTOR, "td.ranktop")
        for item in hotlist:
            if item.text.isdigit():
                atag=item.find_element(By.XPATH, './following-sibling::td[1]/a')
                spantag=item.find_element(By.XPATH, './following-sibling::td[1]/span')
                print(atag.text)
                print(re.search(r'\d+',spantag.text).group())
                # print(contag.get_attribute('href'))

        print(hotlist)
        # time.sleep(5)
