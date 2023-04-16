from rest_framework import serializers
from .models import *

class livenewslistSerializer(serializers.ModelSerializer):
    class Meta:
        model=liveNews
        fields = "__all__"