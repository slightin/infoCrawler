from os import path
import jieba
from PIL import Image
import numpy as np
from wordcloud import WordCloud
from ..models import *


def generate_wordcloud(text, iname):
    # 过jieba进行分词并通过空格分隔, 返回分词后的结果
    jieba_word = jieba.cut(text, cut_all=False)  # cut_all是分词模式，True是全模式，False是精准模式，默认False
    seg_list = ' '.join(jieba_word)

    # 设置显示方式
    d = path.dirname(__file__)
    mask = np.array(Image.open(path.join(d, "images//cloud.png")))
    font_path = path.join(d, "msyh.ttf")
    wc = WordCloud(background_color="white",  # 设置背景颜色
                   max_words=2000,  # 词云显示的最大词数
                   mask=mask,  # 设置背景图片
                   stopwords=set(map(str.strip, open(path.join(d, 'stopwords.dat'), encoding='utf-8').readlines())),
                   # 设置停用词
                   font_path=font_path,  # 兼容中文字体，不然中文会显示乱码
                   )

    # 生成词云
    wc.generate(seg_list)

    # 生成的词云图像保存到本地
    wc.to_file(path.join(d, "images//" + iname + ".png"))


def generate_infocloud():
    acloudtext = ''
    for info in mainNews.objects.order_by("-pub_time")[:100]:
        acloudtext += ' ' + info.title
    generate_wordcloud(acloudtext, 'info')
    for cate in category.objects.all():
        cloudtext = ""
        for info in mainNews.objects.filter(cate=cate).order_by("-pub_time")[:100]:
            cloudtext += ' ' + info.title
        generate_wordcloud(cloudtext, 'info_' + str(cate.id))


def generate_livecloud():
    cloudtext = ''
    for info in liveNews.objects.order_by("-pub_time")[:100]:
        cloudtext += ' ' + info.news_title + ' ' + info.news_content
    generate_wordcloud(cloudtext, 'live')
