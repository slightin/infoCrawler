from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter

from . import views

app_name = "api"

router = DefaultRouter()
router.register('livenews', views.livenewsViewSet)
router.register('hotnews', views.hotnewsViewSet)
router.register('maininfo', views.mainnewsViewSet)
router.register('category', views.cateViewSet)
urlpatterns = [
    path('update', views.update, name='update'),
    path('wordcloud/<str:iname>', views.showcloudimage, name='wordcloud'),
    path('', include(router.urls))
    # path('get/<str:category>', views.getinfo, name='get')
]
