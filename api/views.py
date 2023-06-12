import json
from django.core.serializers import serialize
from django.http import HttpResponse, JsonResponse, Http404
from django.shortcuts import render
from django_filters import rest_framework
from django.views.decorators.csrf import csrf_exempt
from rest_framework.viewsets import ModelViewSet
from .serializers import *
from .filters import *
from .crawler import livenews, hotnews, homenews
from .models import *
from .cloud import *
from os import path
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_job

scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")


@register_job(scheduler, "cron", minute='15,45', id='live', replace_existing=True)
def crawlerLive():
    livenews.lCrawl()
    generate_livecloud()
    print(datetime.datetime.now().strftime('%Y-%m-%d  %H:%M:%S'))
    print("live")


@register_job(scheduler, "cron", minute='*/10', id='hot', replace_existing=True)
def crawlerHot():
    hotnews.gethot()
    print(datetime.datetime.now().strftime('%Y-%m-%d   %H:%M:%S')+'  hot')


@register_job(scheduler, "cron", minute='5', id='main', replace_existing=True)
def crawlerMain():
    homenews.browse()
    generate_infocloud()
    print(datetime.datetime.now().strftime('%Y-%m-%d  %H:%M:%S'))
    print("main")


# scheduler.start()


def get(request, content):
    if content == "carousel":
        carousel = mainNews.objects.exclude(bigimage="").order_by("-pub_time")[:5]
        data = []
        for item in carousel:
            dic = {}
            dic["id"] = item.id
            dic["title"] = item.title
            dic["iurl"] = item.bigimage
            data.append(dic)
        # data = {'list': json.loads(serialize("json", carousel))}
        return HttpResponse(json.dumps(data, ensure_ascii=False))
    else:
        raise Http404


@csrf_exempt
def update(request):
    category = request.POST.get('category')
    if category == "livenews":
        livenews.lCrawl()
    elif category == 'hotnews':
        hotnews.gethot()
    elif category == 'maininfo':
        homenews.browse()

    elif category == 'infocloud':
        generate_infocloud()
    elif category == 'livecloud':
        generate_livecloud()
    else:
        raise Http404
    return HttpResponse("sucess")


def showcloudimage(request, iname):
    d = path.dirname(__file__)
    imagepath = path.join(d, "cloud/images/" + iname + ".png")
    image_data = open(imagepath, "rb").read()
    return HttpResponse(image_data, content_type="image/png")


# @csrf_exempt
# def getinfo(request, category):
#     if category == 'livenews':
#         data = {'list': json.loads(serializers.serialize("json", liveNews.objects.all()))}
#         # data = json.loads(serializers.serialize("json", liveNews.objects.all()))
#         return JsonResponse(data, json_dumps_params={'ensure_ascii': False})

class livenewsViewSet(ModelViewSet):
    queryset = liveNews.objects.all().order_by('-pub_time')
    serializer_class = livenewsSerializer


class hotnewsViewSet(ModelViewSet):
    queryset = hotNews.objects.all().order_by('rank')
    serializer_class = hotnewsSerializer
    filterset_class = hotnewsFilter
    pagination_class = None


class mainnewsViewSet(ModelViewSet):
    queryset = mainNews.objects.all().order_by('-pub_time')
    serializer_class = mainnewsSerializer
    filterset_class = mainnewsFilter


class cateViewSet(ModelViewSet):
    queryset = category.objects.all().order_by('id')
    serializer_class = categorySerializer
    pagination_class = None
