# _*_ coding:utf-8 _*_
# __auth__: LJ
from plugins import plugins_api
import platform


class InfoCollector(object):
    def __init__(self):
        pass

    def collect_data(self):
        os_platform = platform.system()
        os_platform = os_platform.lower()
        if hasattr(self, os_platform):
            func = getattr(self, os_platform)
            return func()

    def linux(self):
        sys_info = plugins_api.get_linux_info()
        return sys_info
    def windows(self):
        sys_info = plugins_api.get_windows_info()
        return sys_info