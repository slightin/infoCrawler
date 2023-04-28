import django_filters
from .models import *


class hotnewsFilter(django_filters.FilterSet):
    class Meta:
        model = hotNews
        fields = ('src',)
