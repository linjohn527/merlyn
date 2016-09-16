# _*_ coding:utf-8 _*_
# __auth__: LJ


from django.core.exceptions import ObjectDoesNotExist
import models
import json
from django.utils import timezone
from  accounts.models import UserProfile

# 用于处理回复的消息类
class Response(object):
    def __init__(self):
        self.response = {
            'error': [],
            'info': [],
            'warning': []
        }

    def add_msg(self, key, msg_type, msg):
        self.response[key].append({msg_type: msg})

    def get_msg(self):
        return self.response

    def clear_error_msg(self):
        self.response['error'] = []

    def has_error_msg(self):
        if len(self.response['error']) > 0:
            return True
        return False


# 此类用于处理客户端发送到此服务器端的资产数据
class AssetHandler(object):
    def __init__(self, request):
        # 初始化数据
        self.request = request
        self.response = Response()
        self.mandatory_check_fields = ['name', 'asset_type'] # 强制检查的数据项

    def check_mandatory_fields(self, data):
        # 检查汇报的资产信息里面的必填项是否存在
        for field in self.mandatory_check_fields:
            if not hasattr(data, field):
                pass
                # self.response.add_msg('error', 'MandatoryCheckFail', 'The field [%s] is mandatory but not provide in report data') % field
        else:
            if self.response.has_error_msg():
                return False

        return True

    def data_is_valid(self):
        # 检查汇报的资产信息里面的必填项是否完整
        data = self.request.POST.get('asset_data')
        if data:
            try:
                json_data = json.loads(data)
                self.check_mandatory_fields(json_data)
                if not self.response.has_error_msg():
                    return True

            except ValueError, e:
                self.response.add_msg('error', 'AssetDataInvalid', str(e))
        else:
            self.response.add_msg('error', 'AssetDataInvalid', 'Reported data is not provided or invalid')

        return False

    def check_asset_obj_exists_in_approval_zone(self, data, only_check_name=True):
        # 检查汇报的资产数据对象是否在待批准入库区
        try:
            if only_check_name:
                new_asset_to_be_approved = models.NewAssetApprovalZone.objects.get(name=data['name'], approved=False)
            else:
                new_asset_to_be_approved = models.NewAssetApprovalZone.objects.get(name=data['name'], sn=data['sn'], approved=False)
            if new_asset_to_be_approved:  # 资产已存在待批准入库区, 等待批准
                print 'new_asset_to_be_approved'
                return True
        except ObjectDoesNotExist:
            print 'asset object [%s] is waited to be approved'
            self.response.add_msg('error', 'AssetToBeApproved', 'asset object [%s] is waited to be approved ' % data['name'])

        return False

    def check_asset_obj_exists_in_assets_zone(self, data, only_check_name=True):
        # 检查汇报的资产数据对象是否已经存在于资产表或者待批准入库表
        try:
            if only_check_name:
                print 'only_check_name'
                self.asset_common_info_obj = models.AssetCommonInfo.objects.get(name=data['name'])
                print self.asset_common_info_obj

            else:
                self.asset_common_info_obj = models.AssetCommonInfo.objects.get(sn=data['sn'], name=['name'])

            if self.asset_common_info_obj: # 资产数据已存在并已批准入库
                return True
        except ObjectDoesNotExist:
            # 资产数据对象还没存到资产表
            self.response.add_msg('error', 'AssetDataInvalid', 'cannot find asset object in DB by using asset name [%s] and SN[%s]' %(data['name'], data['sn']))
            self.waiting_approval = True
        return False

    def prepare_asset_common_data(self):
        # 判断通用资产数据是否是已存在待批准入库区或者是已批准进入资产表，如果数据已经批准入库,则准备资产数据对象asset_common_info_obj
        data = self.request.POST.get('asset_data')
        if data:
            try:
                json_data = json.loads(data)
                if self.data_is_valid(): # 数据有效
                    self.clean_data = json_data
                    if self.check_asset_obj_exists_in_approval_zone(json_data, only_check_name=True): # 资产已存在待批准入库区
                        self.response.add_msg('info', 'asset_id', self.asset_common_info_obj.id) #返回资产的ID
                        return False
                    elif not self.check_asset_obj_exists_in_assets_zone(json_data, only_check_name=True): # 资产数据不存在待批准入库区， 也不存在于已批准的资产区，则说明资产数据从未处理过，首次处理需要添加到待批准入库区
                        print 'not self.check_asset_obj_exists_in_assets_zone'
                        self.response.add_msg('info', 'needs_approval', "this is new aaset, need IT admin's approval to create asset_id")
                        self.save_new_asset_to_approval_zone() # 保存资产数据到待入库区
                        return False
                    elif self.check_asset_obj_exists_in_assets_zone(json_data, only_check_name=True): # 资产数据已批准并且存在于已批准资产区
                        print 'asset data exits'
                        return True

            except Exception, e:
                print 'I am here 4'
                print e.message
                self.response.add_msg('error', 'AssetDataInvalid', str(e))
                return False

        # return self.response.get_msg()

    def save_new_asset_to_approval_zone(self):
        # 保存首次汇报的资产数据到待批准入库区
        try:
            new_asset_in_approval_zone, created = models.NewAssetApprovalZone.objects.get_or_create(
                sn=self.clean_data['sn'],
                name=self.clean_data.get('name'),
                data=json.dumps(self.clean_data),
                manufatory=self.clean_data.get('manufatory'),
                model=self.clean_data.get('model'),
                asset_type=self.clean_data.get('asset_type'),
                ram_size=sum([ ram['capacity'] for ram in self.clean_data.get('ram')]),
                os_distribution=self.clean_data.get('os_distribution'),
                os_release=self.clean_data.get('os_release'),
                os_type=self.clean_data.get('os_type')
            )

        except Exception, e:
            print e
            return False
        return True

    def __is_new_asset(self):
        # 是否是新资产
        if not hasattr(self.asset_common_info_obj, self.clean_data['asset_type'] + 'asset'):
            return True
        else:
            return False


    def __get_or_create_manufatory(self, name):
        # 获取制造商对象
        try:
            obj, created = models.Manufactory.objects.get_or_create(
                name=name
            )
            return obj
        except Exception, e:
            print e.message

        return None

    def __get_or_create_os_info(self, type, distribution, version):
        # 获取软件的对象
        try:
            obj, creaeted = models.Software.objects.get_or_create(
                type=type,
                distribution=distribution,
                version=version
            )
            return obj
        except Exception, e:
            print e.message

        return None

    def save_approved_aseet(self, obj):
        # 添加已经批准的资产
        asset_common_obj = models.AssetCommonInfo(
            name=obj.name,
            sn=obj.sn,
            model=obj.model
        )
        asset_common_obj.manufatory = self.__get_or_create_manufatory(obj.manufatory) # 添加制造商信息
        asset_common_obj.os_info = self.__get_or_create_os_info(type=obj.os_type, distribution=obj.os_distribution, version=obj.os_release)
        asset_common_obj.save() # 保存通用资产信息
        self.save_to_approval_zone_or_update_asset() # 更新或者创建资产信息

    def save_to_approval_zone_or_update_asset(self):
        # 先准备通用的资产数据
        self.response.clear_error_msg()  # 清空错误日志信息
        if self.prepare_asset_common_data(): # 通用的资产数据已存在，并且已批准入库
            # 开始添加(server, networkdevice etc)数据
            print 'save_to_approval_zone_or_update_asset'
            if self.__is_new_asset():
                print 'Going to create new asset'
                self.create_asset() # 创建新资产数据
            else:
                self.update_asset() # 更新新资产数据

    def __verify_field(self, data_set, field_key, data_type, required=True):
        # 验证数据项是否有效
        field_val = data_set.get(field_key)
        if field_val:
            try:
                data_set[field_key] = data_type(field_val)
            except ValueError,e:
                self.response.add_msg('error', 'InvalidField', "The field [%s]'s data type is invalid, the correct data type should be [%s]" %(field_key, data_type))
        elif required:
            self.response.add_msg('error', 'LackOfField', 'The field [%s] has not value in reported data' %field_key)

    def create_asset(self):
        # 根据资产类型创建新资产数据
        print 'create_asset'
        func = getattr(self, '_create_%s' % self.clean_data['asset_type'])
        created_obj = func()

    def update_asset(self):
        # 根据资产类型更新资产数据
        func = getattr(self, '_update_%s' % self.clean_data['asset_type'])
        updat_obj = func()

    def _create_server(self):
        print '_create_server'
        # 创建服务器资产数据
        self.__create_server_info()
        self.__creae_or_update_manufatory()
        self.__create_cpu_component()
        self.__create_ram_component()
        self.__create_disk_component()
        self.__create_nic_component()

    def __create_server_info(self, ignore_errors=True):
        # 创建服务器的基本信息
        try:
            self.__verify_field(self.clean_data, 'model', str)
            if (not self.response.has_error_msg()) or ignore_errors == True:
                os_info, created = models.Software.objects.get_or_create(
                    type=self.clean_data.get('os_type'),
                    distribution=self.clean_data.get('os_distribution'),
                    version=self.clean_data.get('os_release')
                )
                data_set = {
                    'asset_common_info_id': self.asset_common_info_obj.id,
                    'raid_type': self.clean_data.get('raid_type'),
                    'os_info': os_info
                }

                server_obj = models.ServerAsset(**data_set)
                server_obj.save()
                return server_obj
        except Exception, e:
            print e.message
            self.response.add_msg('error', 'ObjectCreateException', str(e))


    def __creae_or_update_manufatory(self, ignore_errors=True):
        # 创建或者更新制造厂商的名称
        try:
            self.__verify_field(self.clean_data, 'manufatory', str)
            manufatory = self.clean_data.get('manufatory')
            if not self.response.has_error_msg() or ignore_errors == True:
                obj_exits = models.Manufactory.objects.filter(name=manufatory)
                if obj_exits:
                    obj = obj_exits[0]
                else:
                    obj = models.Manufactory(name=manufatory)
                    obj.save()
                self.asset_common_info_obj.manufatory = obj
                self.asset_common_info_obj.save()
        except Exception, e:
            self.response.add_msg('error', 'ObjectCreateException', "object [manufatory] %s" % str(e))

    def __create_cpu_component(self, ignore_errors=True):
        # 创建并添加CPU组件
        cpu_list = self.clean_data.get('cpu')
        if cpu_list:
            for cpu_item in cpu_list:
                try:
                    self.__verify_field(cpu_item, 'model', str)
                    # self.__verify_field(cpu_item, 'cpu_count', int)
                    self.__verify_field(cpu_item, 'cpu_core_count', int)
                    self.__verify_field(cpu_item, 'frequency', float)

                    if not self.response.has_error_msg() or ignore_errors == True:
                        print 'save cpu item'
                        manufatory = self.__get_or_create_manufatory(cpu_item.get('manufactory'))
                        data_set = {
                            'asset_common_info_id': self.asset_common_info_obj.id,
                            'model': cpu_item.get('model'),
                            'cpu_core_count': cpu_item.get('cpu_core_count'),
                            'frequency': cpu_item.get('frequency'),
                            'manufatory': manufatory
                        }

                        obj = models.CPU(**data_set)
                        obj.save()
                        log_msg = "Asset[%s] has added new [cpu] component with data [%s]" % (self.asset_common_info_obj, data_set)
                except Exception, e:
                    self.response.add_msg('error', 'ObjectCreateException', "object [cpu] %s" %(str(e)))
        else:
            self.response.add_msg('error', 'LackOfData', "cpu info is not provided in  report")


    def __create_disk_component(self, ignore_errors=True):
        # 创建并添加磁盘组件
        disk_list = self.clean_data.get('disk')
        if disk_list:
            for disk_item in disk_list:
                try:
                    self.__verify_field(disk_item, 'model', str)
                    self.__verify_field(disk_item, 'slot', str)
                    self.__verify_field(disk_item, 'capacity', float)
                    self.__verify_field(disk_item, 'iface_type', str)

                    if not self.response.has_error_msg() or ignore_errors == True:
                        print 'save disk item'
                        data_set = {
                            'asset_common_info_id': self.asset_common_info_obj.id,
                            'sn': disk_item.get('sn'),
                            'model': disk_item.get('model'),
                            'capacity': disk_item.get('capacity'),
                            'slot': disk_item.get('slot'),
                            'iface_type': disk_item.get('iface_type'),
                            'manufatory': self.__get_or_create_manufatory(name=disk_item.get('manufatory'))
                        }

                        obj = models.Disk(**data_set)
                        obj.save()

                except Exception, e:
                    self.response.add_msg('error', 'ObjectCreateException', 'object [disk] %s' % str(e))
        else:
            self.response.add_msg('error', 'LackOfData', "disk info is not provided in report")

        print self.response.get_msg()


    def __create_nic_component(self, ignore_errors=True):
        # 创建并添加网卡组件
        nic_list = self.clean_data.get('nic')
        if nic_list:
            for nic_item in nic_list:
                try:
                    self.__verify_field(nic_item, 'mac_address', str)
                    if not self.response.has_error_msg() or ignore_errors == True:
                        data_set = {
                            'asset_common_info_id': self.asset_common_info_obj.id,
                            'name': nic_item.get('name'),
                            'model': nic_item.get('model'),
                            'manufatory': self.__get_or_create_manufatory(name=nic_item.get('manufatory')) ,
                            'mac_address': nic_item.get('mac_address'),
                            'ip_address': nic_item.get('ipaddress'),
                            'netmask': nic_item.get('netmask'),
                            'bonding_ip': nic_item.get('bonding_ip'),
                            'sn': nic_item.get('sn')
                        }

                        obj = models.NIC(**data_set)
                        obj.save()

                except Exception, e:
                    self.response.add_msg('error', 'ObjectCreateException', 'object [nic] %s' % str(e))

        else:
            self.response.add_msg('error', 'LackOfData', 'nic info is not provided in report')

    def __create_ram_component(self, ignore_errors=True):
        # 创建并添加内存组件
        print self.response.get_msg()
        ram_list = self.clean_data.get('ram')
        if ram_list:
            for ram_item in ram_list:
                try:
                    self.__verify_field(ram_item, 'capacity', int)
                    if not self.response.has_error_msg() or ignore_errors == True:
                        data_set = {
                            'asset_common_info_id': self.asset_common_info_obj.id,
                            'model': ram_item.get('model'),
                            'manufatory': self.__get_or_create_manufatory(name=ram_item.get('manufatory')),
                            'sn': ram_item.get('sn'),
                            'slot': ram_item.get('slot'),
                            'capacity': ram_item.get('capacity')
                        }

                        obj = models.RAM(**data_set)
                        obj.save()

                except Exception, e:
                    self.response.add_msg('error', 'ObjectCreateException', 'object [ram] %s' % str(e))

        else:
            self.response.add_msg('error', 'LackOfData', 'nic info is not provided in report')

    def _update_server(self):
        # 更新服务器组件的资产信息
        self.__update_server_basic_info()
        self.__update_manufatory_component()

        #分别更新网卡，CPU,磁盘，内存组件的资产信息
        try:
            self.__compare_asset_component(data_source=self.clean_data['cpu'],
                                          fk='cpu_set',
                                          update_fields=['slot', 'sn', 'model', 'manufatory', 'frequency', 'cpu_count', 'cpu_core_count'],
                                          identify_field='sn')
            self.__compare_asset_component(data_source=self.clean_data['nic'],
                                          fk='nic_set',
                                          update_fields=['slot', 'name', 'sn', 'model', 'mac_address', 'ip_address', 'netmask', 'bonding_ip', 'manufatory'],
                                          identify_field='mac_address')
            self.__compare_asset_component(data_source=self.clean_data['physical_disk_driver'],
                                          fk='disk_set',
                                          update_fields=['slot', 'sn', 'model', 'manufatory', 'capacity', 'iface_type'],
                                          identify_field='iface_type')
            self.__compare_asset_component(data_source=self.clean_data['ram'],
                                          fk='ram_set',
                                          update_fields=['slot', 'sn', 'model', 'manufatory', 'capacity', 'iface_type'],
                                          identify_field='slot')
        except Exception, e:
            print e.message

    def __update_server_basic_info(self):
        # 更新服务器的基本信息
        update_fields = ['raid_type', 'os_info']
        if hasattr(self.asset_common_info_obj, 'serverasset'):
            self.__compare_and_update_asset_field(self.asset_common_info_obj.serverasset, update_fields, self.clean_data)
        else:
            self.__create_server_info()


    def __update_manufatory_component(self):
        # 更新制造厂商的信息
        self.__creae_or_update_manufatory(ignore_errors=True)



    def __compare_and_update_asset_field(self, model_obj, fields_from_db, data_source):
        # 比较并更新汇报的资产数据与数据库中已有基本数据
        for field in fields_from_db:
            if field == 'os_info': # 因为os_info是一个对象，所以这里要单独比较
                print model_obj.os_info
                os_info = model_obj.os_info
                type_from_db = os_info.type
                distribution_from_db = os_info.distribution
                release_from_db = os_info.version
                type_from_source = data_source.get('os_type')
                distribution_from_source = data_source.get('os_distribution')
                release_from_source = data_source.get('os_release')

                if type_from_db != type_from_source:
                    os_info.type = type_from_source

                if distribution_from_db != distribution_from_source:
                    os_info.distribution = distribution_from_source

                if release_from_db  != release_from_source:
                    os_info.version = release_from_source

                os_info.save()

            else:
                val_from_db = getattr(model_obj, field)
                val_from_source = data_source.get(field)
                if type(val_from_db) in (int, ): val_from_source = int(val_from_source) #数据类型转换
                elif type(val_from_db) is float: val_from_source = float(val_from_source)

                if val_from_db == val_from_source:
                    pass

                else:
                    print 'I am here hahahah'
                    try:
                        db_field = model_obj._meta.get_field(field)
                        db_field.save_form_data(model_obj, val_from_source)
                        model_obj.update_date = timezone.now()
                        model_obj.save()
                        log_msg = "Asset[%s] --> component[%s] --> field[%s] has changed from %s to %s " % (self.asset_common_info_obj, model_obj, field, val_from_db, val_from_source)
                        self.response.add_msg('info', 'FieldChanged', log_msg)
                        log_handler(self.asset_common_info_obj, 'FieldChanged', self.request.user, log_msg, model_obj)
                    except Exception, e:
                        print e.message


    def __compare_asset_component(self, data_source, fk, update_fields, identify_field=None):
        try:
            component_obj = getattr(self.asset_common_info_obj, fk)
            if hasattr(component_obj, 'select_releated'):
                objects_from_db = component_obj.select_releated()
                component_identify_field_val_list_from_db = [] # 数据库中的组件的key值
                for obj in objects_from_db:
                    identify_field_val_from_db = getattr(obj, identify_field)
                    component_identify_field_val_list_from_db.append(identify_field_val_from_db)

                component_identify_field_val_list_from_data_source = [] # 用来汇报数据的组件的key值
                if type(data_source) is list:
                    for data in data_source:
                        identify_field_val_from_data_source = data.get(identify_field)
                        component_identify_field_val_list_from_data_source.append(identify_field_val_from_data_source)

                component_identify_field_val_set_in_db = set(component_identify_field_val_list_from_db) # 转换为集合
                component_identify_field_val_set_in_data_source = set(component_identify_field_val_list_from_data_source) # 转换为集合

                identify_field_val_set_only_in_db =  component_identify_field_val_set_in_db.difference(component_identify_field_val_set_in_data_source)  # 只在数据库而汇报数据中没有的组件key值
                identify_field_val_set_in_both_db_and_data_source = component_identify_field_val_set_in_db.intersection(component_identify_field_val_set_in_data_source) # 同时在数据库和汇报数据中的组件的key值
                identify_field_val_set_only_in_data_source = component_identify_field_val_set_in_data_source.difference(component_identify_field_val_set_in_db)  # 汇报数据有但数据库没有的key值

                if len(identify_field_val_set_only_in_db) > 0 :
                    # 要从数据中删除的组件的identify field值
                    self.__delete_component_from_db(objects_from_db, identify_field, identify_field_val_set_only_in_db)

                if len(identify_field_val_set_only_in_data_source) > 0:
                    # 从汇报的数据中要添加的新组建的信息
                    self.__add_new_component_into_db(component_obj.model._meta.object_name, data_source)

                if len(identify_field_val_set_in_both_db_and_data_source) > 0:
                    # 更新现有数据库的组件信息
                    self.__update_exiting_component_in_db(objects_from_db, data_source, identify_field, identify_field_val_set_in_both_db_and_data_source, update_fields)

        except ValueError as e:
            log_msg = "compare asset component fail: %s" % data_source
            log_handler(self.asset_common_info_obj, 'CompareComponentFail', self.request.user, log_msg)
            print log_msg


    def __update_exiting_component_in_db(self, objects_from_db, data_source, identify_field, identify_field_val_set, update_fields):
        # 更新现有数据库的组件信息
        for obj in objects_from_db:
            for identify_field_val in list(identify_field_val_set):
                if getattr(obj, identify_field) == identify_field_val:
                    self.__compare_and_update_asset_field(obj, update_fields, data_source)


    def __add_new_component_into_db(self, model_obj_name, data_source):
        # 添加新的组件数据
        model_class = getattr(models, model_obj_name)
        for data in data_source:
            try:
                obj = model_class(**data)
                obj.save()
                log_msg = '添加组件:[%s]数据成功' %obj
                log_handler(self.asset_common_info_obj, 'HardwareChanged', self.request.user, log_msg, obj)
            except Exception, e:
                log_msg = '[%s] 添加组件数据:[%s]失败' %(model_obj_name, data)
                log_handler(self.asset_common_info_obj, 'AddNewComponentFail', self.request.user, log_msg)


    def __delete_component_from_db(self, objects_from_db, identify_field, delete_identify_field_val_set):
        # 从数据库删除指定的组件
        try:
            for obj in objects_from_db:
                for identify_field_val in list(delete_identify_field_val_set):
                    if getattr(obj, identify_field) == identify_field_val:
                        obj.delete()
                        log_msg = "Asset[%s] --> component[%s]  has been deleted" % (self.asset_common_info_obj, obj)
                        log_handler(self.asset_common_info_obj, 'HardwareChanged', self.request.user, log_msg, obj)
                        break
        except Exception, e:
            print 'Deleted component fail, error: %s' % str(e)


        def __compare_asset_component2(data_source, fk, update_fields, identify_field=None):
            # 更新资产组件的相关信息
            try:
                component_obj = getattr(self.asset_common_info_obj, fk)
                if hasattr(component_obj, 'select_releated'):
                    objects_from_db = component_obj.select_releated()

                    for obj in objects_from_db:
                        key_field_data = getattr(obj, identify_field)
                        if type(data_source) is list:
                            for source_data_item in data_source:
                                key_field_data_from_source_data = source_data_item.get(identify_field)
                                if key_field_data_from_source_data:
                                    if key_field_data == key_field_data_from_source_data:
                                        self.__compare_and_update_asset_field(obj, update_fields, source_data_item)
                                else:
                                    self.response.add_msg('warning', 'AssetUpdateWarning', 'Asset component [%s] key field [%s] is not provided' %(obj, fk))
                            else:
                                print "Error: can not find any match in source data using key field %s, component data is missing in report data " % key_field_data
                        elif type(data_source) is dict:
                            for key, source_data_item in data_source.items():
                                key_field_data_from_source_data = source_data_item.get(identify_field)
                                if key_field_data_from_source_data:
                                    if key_field_data_from_source_data == key_field_data:
                                        self.__compare_and_update_asset_field(obj, update_fields, source_data_item)
                                        break
                                else:
                                    self.response.add_msg('warning', 'AssetUpdateWarning',
                                                          'Asset component [%s] key field [%s] is not provided' % (
                                                          obj, fk))
                            else:
                                print "Error: can not find any match in source data using key field %s, component data is missing in report data " % key_field_data
                        else:
                            print "error"
            except ValueError, e:
                print str(e)


def log_handler(asset_obj, event_name, user, detail, component=None):
    # 日志记录变更
    log_catelog = {
        1: ['FieldChanged', 'HardwareChanged'],
        2: ['NewComponentAdded'],
        7: ['AddNewComponentFail', 'DeleteComponentFail', 'CompareComponentFail']
    }
    if not user.id:
        user = UserProfile.objects.filter(is_admin=True).last()

    event_type = None
    for k, v in log_catelog.items():
        if event_name in v:
            event_type = k
            break

    log_obj = models.EventLog(
        name=event_name,
        event_type=event_type,
        asset_id=asset_obj.id,
        component=component,
        detail=detail,
        user_id=user.id
    )
    log_obj.save()