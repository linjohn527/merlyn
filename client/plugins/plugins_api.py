# _*_ coding:utf-8 _*_
# __auth__: LJ


from linux import linux_sysinfo
from windows import windows_sysinfo

def get_linux_info():
   sys_info = linux_sysinfo.collect_data()
   return sys_info

def get_windows_info():
    sys_info = windows_sysinfo.collect_data()
    return sys_info