# _*_ coding:utf-8 _*_
# __auth__: LJ

import platform
import win32com
import wmi
import os


def collect_data():
    # 收集windows机器的信息
    data = {
        'os_type': platform.system(),
        'os_release': '%s %s %s' % (platform.release(), platform.architecture()[0], platform.version()),
        'os_distribution': 'Microsoft',
        'asset_type': 'server'
    }

    win_info_obj = WinInfo()
    data.update(win_info_obj.get_cpu_info())
    data.update(win_info_obj.get_server_info())
    data.update(win_info_obj.get_ram_info())
    data.update(win_info_obj.get_disk_info())
    data.update(win_info_obj.get_nic_info())

    resp_data = {
        'status': 0,
        'asset_data': data
    }

    return resp_data

class WinInfo(object):
    def __init__(self):
        self.wmi_obj = wmi.WMI()
        self.wmi_service_obj = win32com.client.Dispatch('WbemScripting.SWbemLocator')
        self.wmi_service_connector = self.wmi_service_obj.ConnectServer('.', 'root\cimv2')

    def get_cpu_info(self):
        cpu_obj_list = self.wmi_obj.Win32_Processor()
        cpu_list = []
        for item in cpu_obj_list:
            item_data = {
                'model': item.Name,
                'cpu_core_count': int(item.NumberOfCores),
                'manufactory': item.Manufacturer,
                'frequency': item.MaxClockSpeed
            }
            cpu_list.append(item_data)

        return {'cpu': cpu_list}

    def get_ram_info(self):
        ram_list = []
        ram_collections = self.wmi_service_connector.ExecQuery('select * from Win32_PhysicalMemory')
        for item in ram_collections:
            mb = int(1024 * 1024)
            ram_size = int(item.Capacity) / mb
            item_data = {
                'sn': item.SerialNumber,
                'manufatory': item.Manufacturer,
                'model': item.Caption,
                'capacity': int(ram_size),
                'slot': item.DeviceLocator.strip()
            }
            ram_list.append(item_data)

        return {'ram': ram_list}


    def get_server_info(self):
        server_info = self.wmi_obj.Win32_ComputerSystem()[0]
        system_info = self.wmi_obj.Win32_OperatingSystem()[0]
        data = {}
        data['manufatory'] = server_info.Manufacturer
        data['model'] = server_info.Model
        data['sn'] = system_info.SerialNumber
        return data


    def get_disk_info(self):
        disk_list = []
        for item in self.wmi_obj.Win32_DiskDrive():
            item_data = {}
            iface_choices = ['SAS', 'SCSI', 'SATA', 'SSD']
            for iface in iface_choices:
                if iface in item.Model:
                    item_data['iface_type'] = iface
                    break

            else:
                item_data['iface_type'] = 'unknown'

            item_data['slot'] = item.Index
            item_data['sn'] = item.SerialNumber.strip()
            item_data['model'] = item.Model
            item_data['manufatory'] = item.Manufacturer
            if item.Size:
                item_data['capacity'] = int(item.Size) / (1024 * 1024 * 1024)
            else:
                item_data['capacity'] = None
            disk_list.append(item_data)

        return {'disk': disk_list}


    def get_nic_info(self):
        nic_list = []
        for item in self.wmi_obj.Win32_NetworkAdapterConfiguration():
            if item.MACAddress is not None:
                item_data = {}
                item_data['mac_address'] = item.MACAddress
                item_data['model'] = item.Caption
                item_data['name'] = item.Index
                if item.IPAddress is not None:
                    item_data['ipaddress'] = item.IPAddress[0]
                    item_data['netmask'] = item.IPSubnet[0]
                else:
                    item_data['ip_address'] = ''
                    item_data['netmask'] = ''
                nic_list.append(item_data)

        return {'nic': nic_list}

if __name__ == '__main__':
    data = collect_data()
    print data