# _*_ coding:utf-8 _*_
# __auth__: LJ

import os
import urllib, urllib2, json
import ConfigParser
from info_collector import InfoCollector

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Arrow(object):
    def __init__(self, argv):
        self.argv = argv
        self.check_argv()

    def help_msg(self):
        print """
            Please input one parameter as below:
            1.collect_data;
            2.report_asset;
            3.run_forever;
        """

    def check_argv(self):
        if len(self.argv) <= 1:
            self.help_msg()
        else:
            if hasattr(self, self.argv[1]):
                func = getattr(self, self.argv[1])
                func()
            else:
                self.help_msg()

    def get_conf_parser(self):
        conf_file_path = BASE_DIR + '/conf/merlyn.conf'
        conf_parser = ConfigParser.ConfigParser()
        conf_parser.read(conf_file_path)
        return conf_parser

    def get_url_and_timeout(self):
        conf_parser = self.get_conf_parser()
        ip = conf_parser.get('server', 'ip')
        port = conf_parser.get('server', 'port')
        timeout = conf_parser.get('server', 'timeout')
        hostname = conf_parser.get('client', 'name')
        url = 'http://' + ip + ':' + port + '/assets/report_asset/'
        return url, timeout, hostname


    def collect_data(self):
        info_collector = InfoCollector()
        asset_data = info_collector.collect_data()
        print asset_data

    def report_asset(self):
        info_collector = InfoCollector()
        resp_data = info_collector.collect_data()
        url, timeout, hostname = self.get_url_and_timeout()
        try:
            # 资产信息中添加主机名信息
            print resp_data
            asset_data = resp_data.pop('asset_data')
            asset_data['name'] = hostname
            asset_data = {
                'asset_data': json.dumps(asset_data)
            }
            resp_data.update(asset_data)
        except Exception, e:
            print e.message

        self.__submit_data(resp_data, url, timeout)

    def __submit_data(self, data, url, timeout, method='POST'):

        if method == 'POST':
            try:
                print url
                encoded_data = urllib.urlencode(data)
                req = urllib2.Request(url=url, data=encoded_data)
                resp_data = urllib2.urlopen(req, timeout=float(timeout))
                callback = resp_data.read()
                callback = json.load(callback)
                print '[%s]:[%s]:[%s]' % (method, url, callback)

            except Exception, e:
                print e.message
