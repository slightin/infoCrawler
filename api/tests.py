import re
import time
import datetime
from bs4 import BeautifulSoup
import json
from django.core import serializers
from django.http import JsonResponse
from django.test import TestCase
from .crawler import crawl, driver_path
from .models import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from .cloud import generate_wordcloud
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CrawlerTests(TestCase):
    def test36hot(self):
        soup = BeautifulSoup(crawl('https://m.36kr.com/hot-list-m'), 'html.parser')
        hot_data = soup.find_all()

    def testsougouhot(self):
        hot_data = json.loads(crawl('https://go.ie.sogou.com/hot_ranks'))
        for item in hot_data["data"]:
            data = item['attributes']
            print(data['rank'])

    def testbaiduhot(self):
        soup = BeautifulSoup(crawl('https://top.baidu.com/board?tab=realtime'), 'html.parser')
        for item in soup.find_all(attrs={"class": "category-wrap_iQLoo horizontal_1eKyQ"}, ):
            print(item.find(attrs={"class": "hot-index_1Bl1a"}).get_text())
            print(item.find(attrs={"class": "c-single-text-ellipsis"}).get_text())
            print(item.find('a').get('href'))

    def testzhihu(self):

        content = crawl("https://www.zhihu.com/billboard")
        soup = BeautifulSoup(content, "html.parser")
        hot_data = soup.find('script', id='js-initialData').string
        print(hot_data)
        hot_json = json.loads(hot_data)
        for index, item in enumerate(hot_json['initialState']['topstory']['hotList'], start=1):
            print(index)
            print(item['target']['titleArea']['text'])

        # for em in soup.find_all(name="a", attrs={"class": "HotList-item"}):
        #     print(em)
        #     print(em.find(attrs={"class": "HotList-itemIndex"}).get_text())
        #     print(em.find(attrs={"class": "HotList-itemTitle"}).get_text())
        #     # print(em.get('data-za-extra-module'))

    def test36krnews_pc(self):
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

    def test36krnews_m(self):
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

    def testjiemian(self):
        content = crawl("https://www.jiemian.com/lists/1325kb.html")
        soup = BeautifulSoup(content, "html.parser")
        date = datetime.datetime.now().strftime("%Y-%m-%d ")
        for item in soup.find_all(attrs={"class": "columns-right-center__newsflash-item"}):
            print(item.get('data-time'))
            print(item.find(attrs={"class": "logStore"}).get_text())
            print(item.find(attrs={"class": "logStore"}).get('href'))
            print(item.find(attrs={"class": "columns-right-center__newsflash-content__summary"}).get_text())


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
        driver = webdriver.Edge(driver_path)
        driver.implicitly_wait(10)
        driver.get('https://s.weibo.com/top/summary?cate=realtimehot')
        hotlist = driver.find_elements(By.CSS_SELECTOR, "td.ranktop")
        for item in hotlist:
            if item.text.isdigit():
                atag = item.find_element(By.XPATH, './following-sibling::td[1]/a')
                spantag = item.find_element(By.XPATH, './following-sibling::td[1]/span')
                print(atag.text)
                print(re.search(r'\d+', spantag.text).group())
                # print(contag.get_attribute('href'))

        print(hotlist)
        # time.sleep(5)


class testmainnews(TestCase):

    def testbrower(self):
        driver = webdriver.Edge(driver_path)
        driver.implicitly_wait(10)

        # 网易
        driver.get('https://news.163.com/')
        for index, nav in enumerate(driver.find_elements(By.CLASS_NAME, 'nav_name')):
            if index == 1 or index == 4:
                continue
            print(nav.text)
            ActionChains(driver).move_to_element(nav).perform()
            time.sleep(0.5)  # 等待hover事件触发
            print(driver.find_elements(By.CSS_SELECTOR,
                                       '.newsdata_item:nth-of-type(' + str(index + 1) + ') .na_pic')[0].get_attribute(
                'href'))
            # for item in driver.find_elements(By.CSS_SELECTOR, '.current .na_pic'):
            #     print(item.get_attribute('href'))
            #     print(item.find_element(By.TAG_NAME, 'img').get_attribute('src'))

        # 36kr
        # krurl = 'https://36kr.com'
        # driver.get(krurl + '/information/shuzihua/')
        # for item in driver.find_elements(By.CLASS_NAME, "tab-item"):
        #     item.click()
        #     driver.find_element(By.CLASS_NAME, 'more-btn-block').click()
        #     # print(atag.get_attribute('href'))
        #     # atag.click()
        #     driver.switch_to.window(driver.window_handles[1])
        #     print(driver.current_url + driver.title)
        #     driver.close()
        #     driver.switch_to.window(driver.window_handles[0])

        time.sleep(3)

    def testkr(self):
        driver = webdriver.Edge(driver_path)
        driver.implicitly_wait(10)

        # 36kr
        krurl = 'https://36kr.com'
        driver.get(krurl + '/information/shuzihua/')
        for item in driver.find_elements(By.CLASS_NAME, "tab-item"):
            item.click()
            driver.find_element(By.CLASS_NAME, 'more-btn-block').click()
            # print(atag.get_attribute('href'))
            # atag.click()
            driver.switch_to.window(driver.window_handles[1])
            print(driver.current_url + driver.title)
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

        # soup = BeautifulSoup(crawl('https://36kr.com/motif/1846745018370696'), 'html.parser')
        # for item in soup.find_all(attrs={"class": "article-item-pic"}):
        #     print(item)
        #     # print(item.find(name='img').get('src'))
        #     print(item.get('href'))
        #     # infosoup = BeautifulSoup(crawl(baseurl + item.get('href')), 'html.parser')

    def testnetease(self):
        soup = BeautifulSoup(crawl('https://www.163.com/dy/article/I47G7AS90514BQ68.html'), 'html.parser')
        # print(soup)
        print(soup.find(attrs={'class': 'post_title'}).get_text())
        print(soup.select_one('.post_body img') is not None)
        print(soup.find(attrs={'class': 'post_info'}).get_text())
        # print(soup.find(attrs={'class': 'post_body'}))
        # for item in soup.find_all(attrs={'class': "newsdata_list"}):
        #     print(item)


class WordcloudTests(TestCase):
    def testinfocloud(self):
        for cates in category.objects.all():
            print(cates)

    def testcloud(self):
        generate_wordcloud('在网上找到一张白色背景的图片下载到当前文件夹，作为词云的背景图（若不指定图片，则默认生成矩形词云）')
