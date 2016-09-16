# _*_ coding:utf-8 _*_
# __auth__: LJ

import models
import json

def fetch_asset_list():
    # 获得所有的资产数据
    print 'I am here2222'
    asset_list = models.AssetCommonInfo.objects.all()
    data_list = []
    print asset_list
    for obj in asset_list:
        common_data =  {
                    'sn': obj.sn,
                    'name': obj.name,
                    'id': obj.id,
                    'model': obj.model,
                    'business_unit': None if not obj.business_unit else obj.business_unit.name,
                    'idc': None if not obj.idc else obj.idc.name,
                    'manufatory': None if not obj.manufatory else obj.manufatory.name,
                    'asset_type': obj.asset_type,
                    'management_ip': obj.management_ip,
                    'status': None
                }
        print common_data
        if hasattr(obj, 'serverasset') or hasattr(obj, 'networkdeviceasset'):
            if obj.asset_type == 'server':
                cpu_list = obj.cpu_set.select_related()
                print cpu_list[0]
                server_data = {
                    'cpu_model': cpu_list[0].model,
                    'cpu_core_count': sum( cpu.cpu_core_count for cpu in cpu_list),
                    'cpu_frequency': cpu_list[0].frequency,
                    'ram_size': sum(i.capacity if i.capacity else 0 for i in obj.ram_set.select_related()),
                    'disk_size': sum(i.capacity if i.capacity else 0 for i in obj.disk_set.select_related())
                }
                common_data.update(server_data)
            elif obj.asset_type in ('switch', 'router', 'firewall', 'storage', 'wireless'):
                network_data = {
                    'cpu_model': None,
                    'cpu_core_count': None,
                    'ram_size': None,
                    'disk_size': None,
                }
                common_data.update(network_data)

            data_list.append(common_data)
    return {'data': data_list}


def fetch_asset_event_logs(asset_id):
    log_list = models.EventLog.objects.filter(asset_id=asset_id)
    data_list = []
    for log in log_list:
        data = {
            'id': log.id,
            'event_type': log.event_type,
            'name': log.name,
            'detail': log.detail,
            'user': log.user.name,
            'date': log.date
        }
        data_list.append(data)
    return {'data': data_list}


class AssetCategory(object):
    def __init__(self, request):
        self.request = request
        self.category_type = self.request.GET.get('category_type')

    def serializer_data(self):
        if hasattr(self, self.category_type):
            category_func = getattr(self, self.category_type)
            data = category_func()
        else:
            data = self.by_asset_type()
        return data

    def by_idc(self):
        print 'by_idc'
        tree = []
        idc_list = models.IDC.objects.all()
        for idc in idc_list:
            asset_type_type = {}
            asset_list = idc.assetcommoninfo_set.select_related()
            idc_node = {
                'text': '%s(%s)' %(idc.name, len(asset_list)),
                'id': idc.id,
                'nodes': []
            }

            for asset_type, asset_type_display_name in models.AssetCommonInfo.asset_type_choices:
                node_objs = asset_list.filter(asset_type=asset_type)
                node_dict = {
                    'text': '%s(%s)' %(asset_type_display_name, len(node_objs)),
                    'id': asset_type,
                    'nodes': []
                }

                for node in node_objs:
                    node_dict['nodes'].append({
                        'text': node.name,
                        'id': node.id,
                        'icon': 'glyphicon glyphicon-stop',
                        'selectedIcon': 'glyphicon glyphicon-stop'
                    })
                idc_node['nodes'].append(node_dict)
            tree.append(idc_node)
        return json.dumps(tree)

    def by_tag(self):
        tree = []
        tag_list = models.AssetTag.objects.all()
        for tag in tag_list:
            asset_list = tag.assetcommoninfo_set.select_related()
            first_layer_node = {
                'text': '%s(%s)' %(tag.name, len(asset_list)),
                'id': tag.id,
                'nodes': []
            }

            for asset in asset_list:
                node_dict = {
                    'text':  asset.name,
                    'id': asset.id,
                    'icon': 'glyphicon glyphicon-stop',
                    'selectedIcon': 'glyphicon glyphicon-stop'
                }
                first_layer_node['nodes'].append(node_dict)

            tree.append(first_layer_node)
        return json.dumps(tree)

    def by_asset_type(self):
        tree = []
        asset_list = models.AssetCommonInfo.objects.all()
        for asset_type, asset_type_display_name in models.AssetCommonInfo.asset_type_choices:
            node_objs = asset_list.filter(asset_type=asset_type)
            node_dict = {
                'text': '%s(%s)' %(asset_type_display_name, len(node_objs)),
                'id': asset_type,
                'nodes': []
            }

            for node in node_objs:
                node_dict['nodes'].append({
                    'text': node.name,
                    'id': node.id,
                    'icon': 'glyphicon glyphicon-stop',
                    'selectedIcon': 'glyphicon glyphicon-stop',
                    'enableLinks': True,
                    'href': '%s' % node.id
                })
            tree.append(node_dict)
        return json.dumps(tree)