import json
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.viewsets import ModelViewSet
from .serializers import *
from .crawler import livenews
from .models import *


@csrf_exempt
def update(request):
    category = request.POST.get('category')
    if category == "livenews":
        livenews.lCrawl()
    return HttpResponse("sucess")


# @csrf_exempt
# def getinfo(request, category):
#     if category == 'livenews':
#         data = {'list': json.loads(serializers.serialize("json", liveNews.objects.all()))}
#         # data = json.loads(serializers.serialize("json", liveNews.objects.all()))
#         return JsonResponse(data, json_dumps_params={'ensure_ascii': False})

class livenewsViewSet(ModelViewSet):
    queryset = liveNews.objects.all()
    serializer_class = livenewslistSerializer