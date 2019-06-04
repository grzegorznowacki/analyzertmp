#!/usr/bin/env python
# -*- coding: utf-8 -*

import requests
from cortexutils.analyzer import Analyzer


# CONFIG
ENDPOINT_HOST = '10.0.2.2'      # for virtualbox connection to localhost on host machine https://superuser.com/questions/144453/virtualbox-guest-os-accessing-local-server-on-host-oscurl
ENDPOINT_PORT = 1234


class SubnetsAnalyzer(Analyzer):
    def __init__(self):
        Analyzer.__init__(self)

    def summary(self, raw):
        taxonomies = []
        taxonomies.append(self.build_taxonomy("info", "SubnetsAnalyzer", "Status", raw['status']))
        return {"taxonomies": taxonomies}

    def query_for_ip_status(self, ip):
        url_all = 'http://' + ENDPOINT_HOST + ':' + str(ENDPOINT_PORT) + '/' + ip + '/all'
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