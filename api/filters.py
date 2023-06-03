import django_filters
from .models import *


class hotnewsFilter(django_filters.FilterSet):
    class Meta:
        model = hotNews
        fields = ('src',)


class mainnewsFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr="icontains")
    pub_gt = django_filters.DateTimeFilter(field_name="pub_time", lookup_expr="gte")
    pub_lt = django_filters.DateTimeFilter(field_name="pub_time", lookup_expr="lte")

    class Meta:
        model = mainNews
        fields = ('cate', 'title', 'pub_time')
