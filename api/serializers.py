from rest_framework import serializers
from .models import *


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """支持动态指定字段的序列化器，传参fields，序列化和反序列化都支持"""
    Meta: type

    def __init__(self, *args, **kwargs):
        """支持字段动态生成的序列化器，从默认的Meta.fields中过滤，无关字段不查不序列化"""
        fields = kwargs.pop('fields', None)
        super().__init__(*args, **kwargs)
        if fields is not None:
            allow = set(fields)
            existing = set(self.fields)
            for f in existing - allow:
                self.fields.pop(f)

    def __new__(cls, *args, **kwargs):
        """list序列化时，首先使用传参的fields，默认用meta.list_fields作为序列化字段"""
        if kwargs.pop('many', False):
            fields = getattr(cls.Meta, 'list_fields', None)
            if fields and 'fields' not in kwargs:
                kwargs['fields'] = fields
            return cls.many_init(*args, **kwargs)
        return super().__new__(cls, *args, **kwargs)


class livenewsSerializer(DynamicFieldsModelSerializer):
    pub_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M')

    class Meta:
        model = liveNews
        fields = '__all__'
        list_fields = ('id', 'news_title', 'pub_time')


class hotnewsSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = hotNews
        fields = '__all__'
        # list_fields = fields


class mainnewsSerializer(DynamicFieldsModelSerializer):
    pub_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    class Meta:
        model = mainNews
        fields = '__all__'
        list_fields = ('id', 'title', 'imageurl', 'pub_time', 'cate', 'intro')
