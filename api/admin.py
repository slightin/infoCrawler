from django.contrib import admin
from .models import *

@admin.register(liveNews)
class liveNewsAdmin(admin.ModelAdmin):
    list_per_page = 30
    search_fields = ('news_title', 'news_content')
    list_display = ('news_title', 'pub_time')
    list_filter = ('pub_time',)
    date_hierarchy = "pub_time"


@admin.register(hotNews)
class hotNewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'src', 'hot')
    list_filter = ('src',)


@admin.register(mainNews)
class mainNewsAdmin(admin.ModelAdmin):
    list_per_page = 30
    search_fields = ('title',)
    list_display = ('title', 'cate', 'pub_time')
    list_filter = ('cate', 'pub_time')
    date_hierarchy = "pub_time"
