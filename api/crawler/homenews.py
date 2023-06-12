import datetime
import re
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from ..models import mainNews, category
from . import crawl, driver_path
from django.db import IntegrityError

krblocklist = []
krurl = 'https://36kr.com'


def crawl_netease(url, imageurl, cate):
    soup = BeautifulSoup(crawl(url), 'html.parser')
    try:
        timeinfo = soup.find(attrs={'class': 'post_info'}).get_text()
        time = re.search(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}', timeinfo).group()
        # pubtime = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M')
        # if pubtime <= lasttime:
        #     return True
        info = mainNews()
        info.imageurl = imageurl
        info.title = soup.find(attrs={'class': 'post_title'}).get_text()
        info.pub_time = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M')
        info.content = str(soup.find(attrs={'class': 'post_body'}))
        if soup.select_one('.post_body img') is not None:
            info.bigimage = soup.select_one('.post_body img').get('src')
        try:
            info.cate = category.objects.get(name=cate)
        except:
            info.cate = category.objects.create(name=cate)
        info.save()
    except IntegrityError as ie:
        print("资讯已存在")
        print(ie)
    except Exception as e:
        print(e)


def browse():
    driver = webdriver.Edge(driver_path)
    driver.implicitly_wait(10)

    # 网易
    driver.get('https://news.163.com/')
    for index, nav in enumerate(driver.find_elements(By.CLASS_NAME, 'nav_name')):
        if index == 1 or index == 4:
            continue
        ActionChains(driver).move_to_element(nav).perform()
        time.sleep(0.5)  # 等待hover事件触发
        for item in driver.find_elements(By.CSS_SELECTOR,
                                         '.newsdata_item:nth-of-type(' + str(index + 1) + ') .na_pic'):
            aurl = item.get_attribute('href')
            iurl = item.find_element(By.TAG_NAME, 'img').get_attribute('src')
            crawl_netease(aurl, iurl, nav.text)

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


# def kr():
#     for item in krblocklist:
#         soup = BeautifulSoup(crawl(item), 'html.parser')
#         for item in soup.find_all(attrs={"class": "article-item-pic"}):
#             info = mainNews()
#             info.imageurl = item.find(name='img').get('src')
#             infosoup = BeautifulSoup(crawl(krurl + item.get('href')), 'html.parser')


def get():
    browse()
