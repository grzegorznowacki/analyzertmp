#!/usr/bin/env python
# -*- coding: utf-8 -*

import requests
from cortexutils.analyzer import Analyzer


# CONFIG
ENDPOINT_HOST = '127.0.0.1'
ENDPOINT_PORT = 1234


class SubnetsAnalyzer(Analyzer):
    def __init__(self):
        Analyzer.__init__(self)

    def query_for_ip_status(self, ip):
        url = 'http://' + ENDPOINT_HOST + ':' + str(ENDPOINT_PORT) + '/' + ip + '/last'
        r = requests.get(url)
        return r.json()

    def result(self):
        if self.data_type == "ip":
            ip = self.get_data()
            res = self.query_for_ip_status(ip)      # class dict - example: {'status': 'U'}
            return res
        else:
            self.error("Wrong data type")

    def run(self):
        self.report(self.result())


if __name__ == '__main__':
    SubnetsAnalyzer().run()