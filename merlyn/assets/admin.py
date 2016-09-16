from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
from .models import *


class ServerInline(admin.TabularInline):
    model = ServerAsset
    exclude = ('memo', )
    readonly_fields = ['create_date']


class CPUInline(admin.TabularInline):
    model = CPU
    exclude = ('memo', )
    readonly_fields = ['create_date']


class RAMInline(admin.TabularInline):
    model = RAM
    exclude = ('memo',)
    readonly_fields = ['create_date']


class NICInline(admin.TabularInline):
    model = NIC
    exclude = ('memo',)
    readonly_fields = ['create_date']


class DiskInline(admin.TabularInline):
    model = Disk
    exclude = ('memo',)
    readonly_fields = ['create_date']


class ComponentInline(admin.TabularInline):
    model = Component
    exclude = ('memo', )
    # inlines = [CPUInline, RAMInline, NICInline, DiskInline]
    readonly_fields = ['create_date']


class AssetCommonInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'asset_type', 'model', 'sn', 'name', 'manufatory', 'management_ip', 'idc', 'business_unit')
    inlines = [ServerInline, CPUInline, RAMInline, NICInline, DiskInline]
    search_fields = ('sn', )
    list_filter = ('idc', 'manufatory', 'business_unit', 'asset_type')


class ComponentAdmin(admin.ModelAdmin):
    list_display = ('name', 'manufatory', 'sn', 'model', 'slot')
    search_fields = ('sn', )
    list_filter = ('name', 'manufatory', 'model', 'slot')


class NICAdmin(admin.ModelAdmin):
    list_display = ('asset_common_info', 'mac_address', 'ip_address', 'bonding_ip')
    search_fields = ('mac_address', 'ip_address')


class EventLogAdmin(admin.ModelAdmin):
    list_display = ('name', 'event_type', 'asset', 'component', 'detail', 'create_date', 'user')
    search_fields = ('asset', )
    list_filter = ('event_type', 'component', 'create_date', 'user')


class NewAssetApprovalZoneAdmin(admin.ModelAdmin):
    actions = ['approval_selected_objects']
    def approval_selected_objects(self, request, queryset):
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        ct = ContentType.objects.get_for_model(queryset.model)
        return HttpResponseRedirect('/assets/new_asset/approval/?ct=%s&ids=%s' %(ct.pk, ','.join(selected)))

admin.site.register(AssetCommonInfo, AssetCommonInfoAdmin)
admin.site.register(ServerAsset)
admin.site.register(NetworkDeviceAsset)
admin.site.register(IDC)
admin.site.register(BusinessUnit)
admin.site.register(Contract)
admin.site.register(CPU)
admin.site.register(RAM)
admin.site.register(Disk)
admin.site.register(NIC, NICAdmin)
admin.site.register(Manufactory)
admin.site.register(AssetTag)
admin.site.register(Software)
admin.site.register(EventLog, EventLogAdmin)
admin.site.register(NewAssetApprovalZone, NewAssetApprovalZoneAdmin)
admin.site.register(Component, ComponentAdmin)
