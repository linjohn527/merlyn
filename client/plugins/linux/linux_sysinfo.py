# _*_ coding:utf-8 _*_
# __auth__: LJ


import platform,  subprocess, re
from collections import OrderedDict

def collect_data():
    basic_sys_info_keys = ['Manufacturer', 'Product Name', 'Serial Number']
    sys_info = {}
    for key in basic_sys_info_keys:
        try:
            cmd_ret = subprocess.check_output("sudo dmidecode -t system | grep '%s'" % key, shell=True)
            cmd_ret = cmd_ret.strip()

            ret_list = cmd_ret.split(':')
            if len(ret_list) > 1:
                sys_info[key] = ret_list[1].strip()
            else:
                sys_info[key] = 'empty'
        except Exception, e:
            print e.message
            sys_info[key] = 'error'

    data = {
        'asset_type': 'server',
        'manufatory': sys_info['Manufacturer'],
        'model': sys_info['Product Name'],
        'sn': sys_info['Serial Number']
    }

    linux_info = LinuxInfo()
    data.update(linux_info.get_os_info())
    data.update(linux_info.get_cpu_info())
    data.update(linux_info.get_ram_info())
    data.update(linux_info.get_nic_info())
    data.update(linux_info.get_disk_info())
    linux_info.get_disk_info()
    print data
    return data


class LinuxInfo(object):
    def __init__(self):
        pass

    def get_cpu_info1(self):
        cpu_list = []
        cmd_ret = subprocess.check_output('cat /proc/cpuinfo', shell=True)
        cmd_ret = cmd_ret.strip()

        processor_list = re.findall('processor', cmd_ret)
        if len(processor_list) > 0:
            cpu_count = len(processor_list)
            cpu_model_list = re.findall('model name.+', cmd_ret)
            cpu_core_count_list = re.findall('cpu cores.+', cmd_ret)
            cpu_frequency_list = re.findall('cpu MHz.+', cmd_ret)
            vendor_id_list = re.findall('vender_id.+', cmd_ret)
            for i in range(cpu_count):
                cpu_model = cpu_model_list[i]
                cpu_model = cpu_model.split(':')[1].strip()
                cpu_core_count = cpu_core_count_list[i]
                cpu_core_count = cpu_core_count.split(':')[1].strip()
                cpu_frequency = cpu_frequency_list[i]
                cpu_frequency = cpu_frequency.split(':')[1].strip()
                vendor_id = vendor_id_list[i]
                vendor_id = vendor_id.split(':')[1].strip()

                cpu_data = {
                    'sn': '',
                    'model': cpu_model,
                    'frequency': cpu_frequency,
                    'manufatory': vendor_id,
                    'cpu_core_count': cpu_core_count
                }
                cpu_list.append(cpu_data)
        return {'cpu': cpu_list}


    def get_cpu_info(self):

        cpu_list = []
        proc_list = []
        proc_info = OrderedDict()

        with open('/proc/cpuinfo') as f:
            for line in f:
                if not line.strip():
                    proc_list.append(proc_info)
                    proc_info = OrderedDict()
                else:
                    if len(line.split(':')) == 2:
                        proc_info[line.split(':')[0].strip()] = line.split(':')[1].strip()
                    else:
                        proc_info[line.split(':')[0].strip()] = ''

        for proc in proc_list:
            proc_data = {
                'model': proc['model name'],
                'manufatory': proc['vendor_id'],
                'cpu_core_count': proc['cpu cores'],
                'frequency': proc['cpu MHz']
            }
            cpu_list.append(proc_data)

        return {'cpu': cpu_list}

    def get_ram_info(self):
        raw_data = subprocess.check_output('sudo dmidecode -t 17', shell=True)
        raw_data_list = raw_data.split('\n')
        raw_ram_list = []
        item_list = []
        ram_list = []

        for line in raw_data_list:
            if line.startswith('Memory Device'):
                raw_ram_list.append(item_list)
            else:
                item_list.append(line.strip())

        for item in raw_ram_list:
            item_ram_size = 0
            ram_dict = {}
            flag = False
            for i in item:
                data = i.split(':')
                if len(data) == 2:
                    k, v = data

                    if k == 'Size':
                        if v.strip() == 'No Module Installed':
                            flag = True
                            break
                        else:
                            ram_dict['capacity'] = v.split()[0].strip()

                    if k == 'Type':
                        ram_dict['model'] = v.strip()

                    if k == 'Manufacturer':
                        ram_dict['manufatory'] = v.strip()

                    if k == 'Serial Number':
                        ram_dict['sn'] = v.strip()

                    if k == 'Locator':
                        ram_dict['slot'] = v.strip()

            if not flag:
                ram_list.append(ram_dict)
            else:
                flag = False

        ram_data = {'ram': ram_list}
        raw_total_ram_size = subprocess.check_output('cat /proc/meminfo | grep MemTotal', shell=True).split(':')
        if len(raw_total_ram_size) == 2:
            ram_size = int(raw_total_ram_size[1].split()[0].strip()) / 1024
            ram_data['ram_size'] = ram_size

        return ram_data

    def get_nic_info(self):
        # cmd_ret = subprocess.check_output('lspci | grep -i eth', shell=True)
        # nic_model = cmd_ret.strip().split()
        raw_data = subprocess.check_output('ifconfig -a', shell=True)
        raw_data = raw_data.split('\n')

        nic_dict = {}
        next_ip_line = False
        last_mac_addr_line = None

        for line in raw_data:
            if next_ip_line:
                next_ip_line = False
                nic_name = last_mac_addr_line.split()[0]
                mac_addr = last_mac_addr_line.split('HWaddr')[1].strip()
                raw_ip_addr = line.split('inet addr:')
                raw_bcast = line.split('Bcast:')
                raw_netmask = line.split('Mask:')
                if len(raw_ip_addr) > 1:
                    ip_addr = raw_ip_addr[1].split()[0]
                    network = raw_bcast[1].split()[0]
                    netmask = raw_netmask[1].split()[0]
                else:
                    ip_addr = None
                    netmask = None
                    netmask = None

                if mac_addr not in nic_dict:
                    nic_dict[mac_addr] = {
                        'name': nic_name,
                        'mac_address': mac_addr,
                        'netmask': netmask,
                        'ip_address': ip_addr,
                        'model': 'unknown',
                        'bonding': 0
                    }

                else:
                    if '%s_bonding_addr' not in nic_dict:
                        random_mac_addr = '%s_bonding_addr' % mac_addr
                    else:
                        random_mac_addr = '%s_bonding2_addr' % mac_addr

                    nic_dict[random_mac_addr] = {
                        'name': nic_name,
                        'mac_address': mac_addr,
                        'netmask': netmask,
                        'network': network,
                        'model': 'unknown',
                        'ip_address': ip_addr
                    }

            if 'HWaddr' in line:
                next_ip_line = True
                last_mac_addr_line = line

        nic_list = []
        for k, v in nic_dict.items():
            nic_list.append(v)

        return {'nic': nic_list}

    def get_os_info(self):
        release = platform.release()
        distribution = ','.join(platform.linux_distribution())
        os_info = {
            'os_type': 'linux',
            'release': release,
            'distribution': distribution
        }

        return os_info

    def get_disk_info(self):
        raw_data = subprocess.check_output('fdisk -l', shell=True)
        raw_data = raw_data.split('\n')
        disk_item_list = []
        for line in raw_data:
            if line.startswith('Disk /dev'):
                raw_disk_info = line.split('Disk')[1].strip().split(':')
                disk_item_list.append((raw_disk_info[0], raw_disk_info[1].split(',')[0].strip())) # 磁盘路径和磁盘容量大小GB
        disk_list = []
        for item in disk_item_list:
            disk_dict = {}
            try:
                raw_disk_data = subprocess.check_output('sudo hdparm -I %s > /dev/null 2>&1' % item[0], shell=True)
                raw_disk_data = raw_disk_data.split('\n')
                for line in raw_disk_data:
                    disk_model = None
                    disk_sn = None
                    if 'Model Number' in line:
                        disk_model = line.split(':')[1].strip()
                    if 'Serial Number' in line:
                        disk_sn = line.split(':')[1].strip()

                    disk_dict = {
                        'name': item[0],
                        'model': disk_model,
                        'sn': disk_sn,
                        'capacity': item[1]
                    }
                disk_list.append(disk_dict)
            except Exception, e:
                pass
        return {'disk': disk_list}

if __name__ == '__main__':
    collect_data()