import json

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import re
from . import driver_path, crawl
from ..models import hotNews
from django.db import connection
from ..cloud import generate_wordcloud

cloudtext = ''


def browse():
    global cloudtext
    driver = webdriver.Edge(driver_path)
    driver.implicitly_wait(10)
    driver.get('https://s.weibo.com/top/summary?cate=realtimehot')
    hotlist = driver.find_elements(By.CSS_SELECTOR, "td.ranktop")
    for item in hotlist:
        if item.text.isdigit():
            atag = item.find_element(By.XPATH, './following-sibling::td[1]/a')
            spantag = item.find_element(By.XPATH, './following-sibling::td[1]/span')
            hot = hotNews()
            hot.src = 'weibo'
            hot.rank = item.text
            hot.title = atag.text
            cloudtext += ' ' + atag.text
            hot.link = atag.get_attribute('href')
            hot.hot = re.search(r'\d+', spantag.text).group()
            hot.save()


def zhihu():
    global cloudtext
    content = crawl("https://www.zhihu.com/billboard")
    soup = BeautifulSoup(content, "html.parser")
    hot_data = soup.find('script', id='js-initialData').string
    hot_json = json.loads(hot_data)
    for index, item in enumerate(hot_json['initialState']['topstory']['hotList'], start=1):
        hot = hotNews()
        hot.rank = index
        title = item['target']['titleArea']['text']
        hot.title = title
        cloudtext += ' ' + title
        hot.src = "zhihu"
        r = re.search(r'\d+', item['target']['metricsArea']['text'])
        if r is None:
            hot.hot = 0
        else:
            hot.hot = r.group() + '0000'
        hot.link = item['target']['link']['url']
        hot.save()


def sogou():
    global cloudtext
    hot_data = json.loads(crawl('https://go.ie.sogou.com/hot_ranks'))
    for item in hot_data["data"]:
        data = item['attributes']
        hot = hotNews()
        hot.src = "sogou"
        title = data["title"]
        cloudtext += ' ' + title
        hot.title = title
        hot.link = "https://www.sogou.com/sie?query=" + title
        hot.hot = data["num"]
        hot.rank = data["rank"]
        hot.save()


def baidu():
    global cloudtext
    soup = BeautifulSoup(crawl('https://top.baidu.com/board?tab=realtime'), 'html.parser')
    for index, item in enumerate(soup.find_all(attrs={"class": "category-wrap_iQLoo horizontal_1eKyQ"}), start=1):
        hot = hotNews()
        hot.rank = index
        hot.src = "baidu"
        hot.hot = (item.find(attrs={"class": "hot-index_1Bl1a"}).get_text())
        title = (item.find(attrs={"class": "c-single-text-ellipsis"}).get_text())
        cloudtext += ' ' + title
        hot.title = title
        hot.link = (item.find('a').get('href'))
        hot.save()


def gethot():
    # hotNews.objects.all().delete()
    # hotNews.objects.raw('AUTO_INCREMENT = 1;')
    # 重置表
    cursor = connection.cursor()  # 用建立好的connection对象创建cursor游标对象
    cursor.execute("truncate table api_hotnews")  # 执行自定义SQL语句
    cursor.close()  # 执行完，关闭
    connection.commit()
    connection.close()

    browse()
    zhihu()
    baidu()
    sogou()
    generate_wordcloud(cloudtext, 'hot')
