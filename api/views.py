import json

from django.core import serializers
from django.http import HttpResponse, JsonResponse, Http404
from django.shortcuts import render
from django_filters import rest_framework
from django.views.decorators.csrf import csrf_exempt
from rest_framework.viewsets import ModelViewSet
from .serializers import *
from .filters import *
from .crawler import livenews, hotnews, homenews
from .models import *
from os import path


@csrf_exempt
def update(request):
    category = request.POST.get('category')
    if category == "livenews":
        livenews.lCrawl()
    elif category == 'hotnews':
        hotnews.gethot()
    elif category == 'maininfo':
        homenews.browse()
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