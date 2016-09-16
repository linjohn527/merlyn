# coding: utf-8

from django.shortcuts import render
from django.http import HttpResponse
from core import AssetHandler
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
import json
import models
import data_format_handler
import utlis

# Create your views here.
def report_asset(request):
    # 资产数据汇报
    asset_handler = AssetHandler(request)
    if asset_handler.data_is_valid(): # 汇报的资产数据有效
        asset_handler.save_to_approval_zone_or_update_asset() # 插入资产数据到DB

    return HttpResponse(json.dumps(asset_handler.response.get_msg()))


@login_required
def approval_new_asset(request):
    # 批准新资产入库
    if request.method == 'POST':
        request.POST = request.POST.copy()
        approved_asset_id_list = request.POST.getlist('approved_asset_list')
        approved_asset_list = models.NewAssetApprovalZone.objects.filter(id__in=approved_asset_id_list)

        response_dict = {}
        for obj in approved_asset_list:
            request.POST['asset_data'] = obj.data
            asset_handler = AssetHandler(request)
            if asset_handler.data_is_valid():
                obj.approved = True
                obj.approved_by = request.user
                obj.save()
            asset_handler.save_approved_aseet(obj) # 保存已批准的通用资产信息
            response_dict[obj.id] = asset_handler.response.get_msg()

        return render(request, 'assets/new_assets_approval.html', {'new_assets': approved_asset_list, 'response_dict': response_dict})

    elif request.method == 'GET':
        ids = request.GET.get('ids')
        id_list = ids.split(',')
        new_asset_list = models.NewAssetApprovalZone.objects.filter(id__in=id_list)
        return render(request, 'assets/new_assets_approval.html', {'new_assets': new_asset_list})


@login_required
def display_asset_list(request):
    # 返回资产列表
    print 'display_asset_list'
    return render(request, 'assets/assets.html')


@login_required
def fetch_asset_list(request):
    # 返回格式化的资产数据
    print 'fetch_asset_list'
    asset_dict = data_format_handler.fetch_asset_list()
    print asset_dict
    return HttpResponse(json.dumps(asset_dict, default=utlis.json_date_handler))


@login_required
def asset_category(request):
    # 获取资产数据
    category_type = request.GET.get('category_type')
    if not category_type: category_type = 'server'
    if request.is_ajax():
        pass


@login_required
def display_asset_detail(request, asset_id):
    # 根据资产的ID获取资产信息并展示
    if request.method == 'GET':
        try:
            asset_obj = models.AssetCommonInfo.objects.get(id=asset_id)
        except ObjectDoesNotExist, e:
            return render(request, 'assets/asset_detail.html', {'error': e})

        return render(request, 'assets/asset_detail.html', {'asset_obj': asset_obj})


@login_required
def fetch_asset_detail(request, asset_id):
    # 根据资产的ID获取资产信息
    if request.method == 'GET':
        try:
            asset_obj = models.AssetCommonInfo.objects.get(id=asset_id)
        except ObjectDoesNotExist, e:
            return render(request, 'assets/asset_category.html', {'error': e})

        return render(request, 'assets/asset_category.html', {'asset_obj': asset_obj})


@login_required
def fetch_asset_event_logs(request, asset_id):
    # 获取事件日志记录
    print 'fetch_asset_event_logs'
    print asset_id
    if request.method == 'GET':
        log_list = data_format_handler.fetch_asset_event_logs(asset_id)
        return HttpResponse(json.dumps(log_list, default=utlis.json_datetime_handler))


@login_required
def fetch_asset_category(request):
    # 获取类别数据，展示类别数据
    category_type = request.GET.get('category_type')
    if not category_type:
        category_type = 'server'

    if request.is_ajax():
        category = data_format_handler.AssetCategory(request)
        data = category.serializer_data()
        return HttpResponse(data)
    else:
        return render(request, 'assets/asset_category.html', {'category_type': category_type})