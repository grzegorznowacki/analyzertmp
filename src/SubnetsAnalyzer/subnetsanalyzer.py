#!/usr/bin/env python
# -*- coding: utf-8 -*

import requests
from cortexutils.analyzer import Analyzer

class SubnetsAnalyzer(Analyzer):
    def __init__(self):
        Analyzer.__init__(self)

        self.host = self.get_param(
            'config.host',
            None,
            'No endpoint host for analyzer given. Please add it to the cortex configuration.'
        )
        self.port = self.get_param(
            'config.port',
            None,
            'No endpoint port for analyzer given. Please add it to the cortex configuration.'
        )

    def summary(self, raw):
        taxonomies = []
        taxonomies.append(self.build_taxonomy("info", "ip", "stat", raw['status']))
        return {"taxonomies": taxonomies}

    def query_for_ip_status(self, ip):
        url_all = 'http://' + self.host + ':' + self.port + '/' + ip + '/all'
        r = requests.get(url_all).json()
        res = {}
        if isinstance(r,(list,)):      
            res['status'] = r[0]['status']
            res['last'] = r[0]
            res['all'] = r
        else:
            res['status'] = r['status']
        return res

    def result(self):
        if self.data_type == "ip":
            ip = self.get_data()
            res = self.query_for_ip_status(ip)
            return res
        else:
            self.error("Wrong data type")

    def run(self):
        self.report(self.result())


if __name__ == '__main__':
    SubnetsAnalyzer().run()