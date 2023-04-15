from django.urls import path

from . import views

app_name = "api"

urlpatterns = [
    path('update', views.update, name='update'),
    path('get/<str:category>', views.getinfo, name='get')
]