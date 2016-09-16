# _*_ coding:utf-8 _*_
# __auth__: LJ

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.UserProfileListAPIView.as_view(), name='list')
]