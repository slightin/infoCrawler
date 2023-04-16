from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter

from . import views

app_name = "api"

router = DefaultRouter()
router.register('livenews', views.livenewsViewSet)
urlpatterns = [
    path('update', views.update, name='update'),
    path('', include(router.urls))
    # path('get/<str:category>', views.getinfo, name='get')
]
