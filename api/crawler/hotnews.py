from selenium import webdriver
from selenium.webdriver.common.by import By
import re
from . import driver_path
from ..models import hotNews

def weibo():
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
            hot.link = atag.get_attribute('href')
            hot.hot = re.search(r'\d+', spantag.text).group()
            # print(atag.text)
            # print(re.search(r'\d+', spantag.text).group())
            # print(contag.get_attribute('href'))
            hot.save()
