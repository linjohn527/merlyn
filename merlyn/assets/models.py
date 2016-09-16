# _*_ coding:utf-8 _*_

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from django.db import models
from accounts.models import UserProfile

# Create your models here.


class Manufactory(models.Model):
    # 硬件制造厂家
    name = models.CharField(u'厂商名称', max_length=64, unique=True)
    support_num = models.CharField(u'服务电话', max_length=30, blank=True, null=True)
    memo = models.TextField(u'备注信息', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'厂商'
        verbose_name_plural = u'厂商'


class BusinessUnit(models.Model):
    parent_unit = models.ForeignKey('self', related_name='parent_level', blank=True, null=True)
    name = models.CharField(u'业务线', max_length=64, unique=True)
    memo = models.TextField(u'备注', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'业务线'
        verbose_name_plural = u'业务线'


class Contract(models.Model):
    contract_no = models.CharField(u'合同号', max_length=128, unique=True)
    name = models.CharField(u'合同名称', max_length=128)
    memo = models.CharField(u'备注', max_length=128, blank=True, null=True)
    price = models.IntegerField(u'合同金额')
    detail = models.TextField(u'合同详细', blank=True, null=True)
    start_date = models.DateField(u'合同开始时间', blank=True)
    end_date = models.DateField(u'合同结束时间', blank=True)
    license_num = models.IntegerField(u'license数量', blank=True)
    create_date = models.DateField(auto_now_add=True)
    update_date = models.DateField(auto_now=True)

    class Meta:
        verbose_name = u'合同'
        verbose_name_plural = u'合同'

    def __str__(self):
        return self.name


class IDC(models.Model):
    name = models.CharField(u'机房名称', max_length=64, blank=True)
    memo = models.CharField(u'备注', max_length=128, blank=True, null=True)

    class Meta:
        verbose_name = u'机房'
        verbose_name_plural = u'机房'

    def __str__(self):
        return self.name


class AssetTag(models.Model):
    name = models.CharField(u'资产标签名称', max_length=64, unique=True)
    creator = models.ForeignKey(UserProfile)
    create_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'资产标签'
        verbose_name_plural = u'资产标签'


class EventLog(models.Model):
    name = models.CharField(u'事件名称', max_length=128)
    event_type_choices = (
        (1, u'硬件变更'),
        (2, u'新增配件'),
        (3, u'设备上线'),
        (4, u'设备下线'),
        (5, u'定期维护'),
        (6, u'业务上线\更新\变更'),
        (7, u'其它')
    )
    event_type = models.SmallIntegerField(u'事件类型', choices=event_type_choices)
    asset = models.ForeignKey('AssetCommonInfo')
    component = models.CharField(u'事件子项', max_length=255, null=True, blank=True)
    detail = models.TextField(u'事件详情')
    create_date = models.DateTimeField(u'事件创建时间', auto_now_add=True)
    user = models.ForeignKey(UserProfile, verbose_name=u'事件源')
    memo = models.CharField(u'备注', null=True, blank=True, max_length=128)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'事件'
        verbose_name_plural = u'事件'


class Software(models.Model):
    # 操作系统,软件,固件版本相关
    type_choices = (
        ('linux', 'Linux'),
        ('windows', 'Windows'),
        ('network_firmware', 'Network Firmware'),
        ('software', 'Software')
    )
    os_distribution_choices = (
        ('windows', 'Windows'),
        ('centos', 'Centos'),
        ('ubuntu', 'Ubuntu')
    )
    language_choices = (
        ('cn', u'中文'),
        ('en', u'英文')
    )
    type = models.CharField(u'软件类型', max_length=64, choices=type_choices, help_text=u'eg.GNU/Linux', default=1)
    distribution = models.CharField(u'发行版本', max_length=32, choices=os_distribution_choices, default='windows')
    version = models.CharField(u'软件/系统版本', max_length=32, unique=True)
    language = models.CharField(u'软件/系统语言', max_length=32, default='cn', choices=language_choices)

    def __str__(self):
        return self.version

    class Meta:
        verbose_name = u'软件/系统'
        verbose_name_plural = u'软件/系统'


class AssetCommonInfo(models.Model):
    # 资产通用的信息
    asset_type_choices = (
        ('server', u'服务器'),
        ('switch', u'交换机'),
        ('router', u'路由器'),
        ('firewall', u'防火墙'),
        ('wireless', u'无线设备'),
        ('storage', u'存储设备'),
        ('software', u'软件资产'),
        ('other', u'其它资产')
    )

    asset_type = models.CharField(max_length=64, choices=asset_type_choices, default='server')
    name = models.CharField(max_length=64, unique=True)
    model = models.CharField(u'型号', max_length=128, null=True, blank=True)
    sn = models.CharField(u'资产SN号', max_length=128, unique=True)
    manufatory = models.ForeignKey('Manufactory', verbose_name=u'制造厂商')
    management_ip = models.GenericIPAddressField(u'管理IP', null=True, blank=True)
    contract = models.ForeignKey('Contract', verbose_name=u'合同', null=True, blank=True)
    purchase_date = models.DateField(u'购买时间', null=True, blank=True)
    expired_date = models.DateField(u'过保时间', null=True, blank=True)
    price = models.IntegerField(u'购买价格', null=True, blank=True)
    business_unit = models.ForeignKey('BusinessUnit', verbose_name=u'所属业务线', null=True, blank=True)
    admin = models.ForeignKey(UserProfile, verbose_name=u'资产管理员', null=True, blank=True)
    idc = models.ForeignKey('IDC', verbose_name=u'所属机房', null=True, blank=True)
    tags = models.ManyToManyField('AssetTag', blank=True)
    memo = models.TextField(u'备注', null=True, blank=True)
    create_date = models.DateTimeField(u'创建时间', blank=True, auto_now_add=True)
    update_date = models.DateTimeField(u'更新时间', blank=True, auto_now=True)

    class Meta:
        verbose_name = u'资产通用信息'
        verbose_name_plural = u'资产通用信息'

    def __str__(self):
        return self.name


class ServerAsset(models.Model):
    asset_common_info = models.OneToOneField('AssetCommonInfo')
    created_by_choices = (
        ('auto', 'Auto'),
        ('manual', 'Manual')
    )
    created_by = models.CharField(max_length=32, choices=created_by_choices, default='auto')
    hosted_on = models.ForeignKey('self', null=True, blank=True, related_name='hosted_on_server')
    raid_type = models.CharField(u'raid类型', null=True, blank=True, max_length=128)
    os_info = models.ForeignKey('Software')
    # os_type = models.CharField(u'操作系统类型', null=True, blank=True, max_length=64)
    # os_distribution = models.CharField(u'发行版本号', max_length=64, null=True, blank=True)
    # os_release = models.CharField(u'操作系统版本', max_length=64, null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True, blank=True)
    update_date = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        verbose_name = u'服务器'
        verbose_name_plural = u'服务器'

    def __str__(self):
        return self.asset_common_info.name


class NetworkDeviceAsset(models.Model):
    asset_common_info = models.OneToOneField('AssetCommonInfo')
    firmware = models.ForeignKey('Software')
    port_num = models.SmallIntegerField(u'端口数量', null=True, blank=True)
    device_detail = models.TextField(u'设备详情', null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True, blank=True)
    update_date = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        verbose_name = u'网络设备'
        verbose_name_plural = u'网络设备'


class Component(models.Model):
    # common_asset_info = models.ForeignKey('AssetCommonInfo')
    name = models.CharField(u'名称', max_length=64, blank=True, null=True)
    manufatory = models.ForeignKey(u'Manufactory', null=True, blank=True)
    model = models.CharField(u'型号', max_length=128, blank=True)
    sn = models.CharField(u'SN号', max_length=128, null=True, blank=True)
    slot = models.CharField(u'插槽号', max_length=64, null=True, blank=True)
    memo = models.TextField(u'备注', null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        verbose_name = u'组件的通用信息'
        verbose_name_plural = u'组件的通用信息'

    def __str__(self):
        return self.model


class CPU(Component):
    asset_common_info = models.ForeignKey('AssetCommonInfo')
    #component_common_info = models.OneToOneField('Component')
    # cpu_model = models.CharField(u'CPU型号', max_length=128, blank=True)
    #cpu_count = models.SmallIntegerField(u'CPU物理个数')
    cpu_core_count = models.SmallIntegerField(u'CPU核个数')
    frequency = models.CharField(u'主频', max_length=32, null=True, blank=True)
    # memo = models.TextField(u'备注', blank=True, null=True)
    # create_date = models.DateTimeField(auto_now_add=True)
    # update_date = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        verbose_name = u'CPU部件'
        verbose_name_plural = u'CPU部件'

    def __str__(self):
        return self.model


class RAM(Component):
    asset_common_info = models.ForeignKey('AssetCommonInfo')
    # sn = models.CharField(u'SN号', max_length=128, null=True, blank=True)
    # model = models.CharField(u'内存型号', max_length=128)
    # component_common_info = models.OneToOneField('Component')
    # slot = models.CharField(u'插槽号', max_length=64)
    capacity = models.IntegerField(u'内存大小(Mb)')
    # memo = models.CharField(u'备注', max_length=128, null=True, blank=True)
    # create_date = models.DateTimeField(auto_now_add=True, blank=True)
    # update_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return '%s:%s:%s' %(self.asset_common_info.id, self.slot, self.capacity)

    class Meta:
        verbose_name = 'RAM'
        verbose_name_plural = 'RAM'
        # unique_together = ('common_asset_info', 'slot')
    auto_create_fields = ['sn', 'slot', 'model', 'capacity']


class Disk(Component):
    asset_common_info = models.ForeignKey('AssetCommonInfo')
    # component_common_info = models.OneToOneField('Component')
    # sn = models.CharField(u'SN号', max_length=128, null=True, blank=True)
    # slot = models.CharField(u'插槽号', max_length=64)
    capacity = models.IntegerField(u'磁盘容量(GB)', blank=True, null=True)

    disk_iface_choices = (
        ('SATA', 'SATA'),
        ('SAS', 'SAS'),
        ('SCSI', 'SCSI'),
        ('SSD', 'SSD')
    )
    iface_type = models.CharField(u'接口类型', max_length=64, choices=disk_iface_choices, default='SAS')
    auto_create_fields = ['sn', 'slot', 'manufatory', 'model', 'capacity', 'iface_type']

    class Meta:
        verbose_name = u'磁盘'
        verbose_name_plural = u'磁盘'
        # unique_together = ('common_asset_info', 'slot')

    def __str__(self):
        return '%s:slot:%s:capacity:%s' %(self.asset_common_info.id, self.slot, self.capacity)


class NIC(Component):
    asset_common_info = models.ForeignKey('AssetCommonInfo')
    # component_common_info = models.OneToOneField('Component')
    mac_address = models.CharField(u'物理地址', max_length=64, unique=True)
    ip_address = models.GenericIPAddressField(u'IP', null=True, blank=True)
    netmask = models.CharField(u'掩码', max_length=64, null=True, blank=True)
    bonding_ip = models.CharField(u'绑定IP', max_length=64, null=True, blank=True)
    auto_create_fields = ['name', 'sn', 'model', 'mac_address', 'ipa_ddress', 'bonding_ip']

    class Meta:
        verbose_name = u'网卡'
        verbose_name_plural = u'网卡'

    def __str__(self):
        return '%s:%s' %(self.asset_common_info.id, self.mac_address)


class RaidAdaptor(Component):
    asset_common_info = models.ForeignKey('AssetCommonInfo')
    # component_common_info = models.OneToOneField('Component')

    class Meta:
        verbose_name = 'RaidAdaptor'
        verbose_name_plural = 'RaidAdaptor'

    def __str__(self):
        return self.name


class NewAssetApprovalZone(models.Model):
    asset_type_choices = (
        ('server', u'服务器'),
        ('switch', u'交换机'),
        ('router', u'路由器'),
        ('firewall', u'防火墙'),
        ('storage', u'存储设备'),
        ('wireless',u'无线设备'),
        ('software', u'软件资产'),
        ('other', u'其他资产')
    )
    name = models.CharField(u'资产名称', max_length=128, unique=True)
    sn = models.CharField(u'资产SN号', max_length=128, unique=True)
    asset_type = models.CharField(u'资产类型', max_length=64, choices=asset_type_choices, null=True, blank=True)
    manufatory = models.CharField(u'制造厂商', max_length=64, null=True, blank=True)
    model = models.CharField(u'型号', max_length=128, null=True, blank=True)
    ram_size = models.IntegerField(null=True, blank=True)
    os_distribution = models.CharField(max_length=64, null=True, blank=True)
    os_type = models.CharField(max_length=64, null=True, blank=True)
    os_release = models.CharField(max_length=64, null=True, blank=True)
    data = models.TextField(u'资产数据')
    report_date = models.DateTimeField(u'数据汇报日期', auto_now_add=True)
    approved = models.BooleanField(u'是否批准', default=False)
    approved_by = models.ForeignKey(UserProfile, verbose_name=u'批准人', null=True, blank=True)
    approved_date = models.DateTimeField(u'批准日期', null=True, blank=True, auto_now=True)

    class Meta:
        verbose_name = u'新上线待批准资产'
        verbose_name_plural = u'新上线待批准资产'

    def __str__(self):
        return self.sn





