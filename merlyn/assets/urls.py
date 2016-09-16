"""merlyn URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
import views


urlpatterns = [
    url(r'^report_asset/$', views.report_asset),
    url(r'asset_list/$', views.display_asset_list, name='asset_list'),
    url(r'asset_list/(\d+)/$', views.display_asset_detail, name='asset_detail'),
    url(r'asset_list/list/$', views.fetch_asset_list, name='fetch_asset_list'),
    url(r'asset_list/category/(\d+)/$', views.fetch_asset_detail, name='fetch_asset_detail'),
    url(r'asset_list/category/$', views.fetch_asset_category, name='asset_category'),
    url(r'asset_event_logs/(\d+)/$', views.fetch_asset_event_logs, name='asset_event_logs'),
    url(r'^new_asset/approval/$', views.approval_new_asset),

]
