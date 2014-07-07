#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2014, DataCanvasIO
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are
# permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this list of
#    conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice, this list
#    of conditions and the following disclaimer in the documentation and/or other
#    materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors may be
#    used to endorse or promote products derived from this software without specific
#   prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
# OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT
# SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
# TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH
# DAMAGE.

"""
A mini sqoop2 REST api library.
"""
__version__ = "0.0.1"
__author__ = "xiaolin"

import requests
import json
import copy
import urllib

import time

def current_milli_time():
    return int(round(time.time() * 1000))

class MySqoop(object):
    def __init__(self, host, port):
        self._svc_root = "http://%s:%s/sqoop" % (host, port)

    def version(self):
        return requests.get(self._svc_root + "/version").json()

    def connection(self, xid=None):
        if not xid:
            return requests.get(self._svc_root + "/v1/connection/all").json()
        else:
            return requests.get(self._svc_root + "/v1/connection/%s" % str(xid)).json()

    def connector(self, cid=None):
        if not cid:
            return requests.get(self._svc_root + "/v1/connector/all").json()
        else:
            return requests.get(self._svc_root + "/v1/connector/%s" % str(cid)).json()

    def get_connection_by_name(self, name):
        conn_dict = {c['name']:c for c in self.connection()['all']}
        if name not in conn_dict:
            raise Exception("Sqoop2 Connection '%s' not found" % name)
        return conn_dict[name]

    def create_connection(self, name, framework_params, connector_params):
        r = self.framework()
        framework_import_form = copy.deepcopy(r['con-forms'])
        for f in framework_import_form:
            for fi in f['inputs']:
                if fi['name'] in framework_params:
                    fi['value'] = urllib.quote(framework_params[fi['name']], '')

        connector = self.connector()['all'][0]
        connector_forms = copy.deepcopy(connector['con-forms'])
        pp(connector_forms)
        for c in connector_forms:
            for ci in c['inputs']:
                if ci['name'] in connector_params:
                    ci['value'] = urllib.quote(connector_params[ci['name']], '')

        now_time = current_milli_time()
        new_d = {
            "id": -1,
            "enable": True,
            "updated": now_time,
            "created": now_time,
            "name": name,
            "connector": connector_forms,
            "connector-id": connector['id'],
            "framework": framework_import_form
        }
        all_d = { "all": [ new_d ] }
        r = requests.post(self._svc_root + "/v1/connection", data=json.dumps(all_d), headers={'content-type': 'application/json'})
        if r.status_code != 200:
            print("--------------------")
            pp(all_d)
            pp(r.status_code)
            pp(r.text)
            raise Exception("Failed to create a connection")
        else:
            return r.json()

    def framework(self):
        return requests.get(self._svc_root + "/v1/framework").json()

    def get_job(self, jid=None):
        if not jid:
            return requests.get(self._svc_root + "/v1/job/all").json()
        else:
            return requests.get(self._svc_root + "/v1/job/" + str(jid)).json()

    def create_import_job(self, job_name, connection_name, framework_params, job_params):
        r = self.framework()
        framework_import_form = copy.deepcopy(r['job-forms']['IMPORT'])
        for f in framework_import_form:
            for fi in f['inputs']:
                if fi['name'] in framework_params:
                    fi['value'] = urllib.quote(framework_params[fi['name']], '')

        connection = self.get_connection_by_name(connection_name)
        connector = self.connector(connection['connector'][0]['id'])
        connector_job_form = copy.deepcopy(connector['all'][0]['job-forms']['IMPORT'])
        for c in connector_job_form:
            for ci in c['inputs']:
                if ci['name'] in job_params:
                    ci['value'] = urllib.quote(job_params[ci['name']], '')

        now_time = current_milli_time()
        new_d = {
            'connection-id': connection['id'],
            'connector': connector_job_form,
            'connector-id': 1,
            "creation-date": now_time,
            "creation-user": None, 
            "enabled": True, 
            "framework": framework_import_form,
            "id": -1, 
            "name": job_name,
            "type": "IMPORT", 
            "update-date": now_time,
            "update-user": None
        }

        all_d = { "all":[ new_d ] }
        r = requests.post(self._svc_root + "/v1/job", data=json.dumps(all_d), headers={'content-type': 'application/json'})
        if r.status_code != 200:
            pp(all_d)
            raise Exception("Failed to create a import job")
        else:
            return r.json()

    def delete_job(self, jid):
        r = requests.delete(self._svc_root + "/v1/job/" + str(jid))
        if r.status_code != 200:
            raise Exception("Failed to delete a import job: '%s', status_code=%s" % (str(jid), r.status_code))
        else:
            return r.json()

    def delete_all_jobs(self):
        jobs = self.get_job()
        for j in jobs['all']:
            self.delete_job(j['id'])

    def run_job(self, jid):
        r = requests.post(self._svc_root + "/v1/submission/action/" + str(jid))
        if r.status_code != 200:
            raise Exception("Failed to run a job: '%s'" % str(jid))
        else:
            return r.json()

    def wait_job(self, jid):
        while True:
            time.sleep(1)
            r = requests.get(self._svc_root + "/v1/submission/history/" + str(jid))
            if r.status_code != 200:
                raise Exception("Failed to run a job: '%s'" % str(jid))

            pp(r.json())
            if r.json()['all'][0]['status'] in ['FAILURE_ON_SUBMIT']:
                raise Exception("Failed to run a job: '%s'" % str(jid))
                
            if r.json()['all'][0]['status'] in ['SUCCEEDED', 'UNKNOWN']:
                return r

def pp(j):
    print(json.dumps(j, indent=4, sort_keys=True))

def main():
    sqoop = MySqoop("192.168.1.20", 12000)
    # pp(sqoop.get_job())
    # print(sqoop.version())
    # pp(sqoop.connection(1))
    # pp(sqoop.connector(1))
    # pp(sqoop.get_xid_by_name("zdwechat message"))
    # pp(sqoop.get_xid_by_name("xxx"))
    # r = sqoop.create_job()
    # r = sqoop.framework()
    # pp(r)
    # sqoop.delete_all_jobs()


    fw_ps = {
        "output.storageType": "HDFS",
        "output.outputFormat": "TEXT_FILE",
        "output.outputDirectory": "/tmp/jiaqi/messageh"
    }
    job_ps = {
        "table.sql": "select UserId,Description,RefreshDate from Message where ${CONDITIONS}",
        "table.partitionColumn": "UserId"
    }
    r = sqoop.create_import_job(job_name="zdwechat message",
                                connection_name="zdwechat message",
                                framework_params=fw_ps,
                                job_params=job_ps)
    pp(r)
    sqoop.run_job(r['id'])
    sqoop.wait_job(r['id'])
    # sqoop.delete_job(r['id'])

    # fw_ps = {
    # }
    # co_ps = {
    #     "connection.jdbcDriver": "com.microsoft.sqlserver.jdbc.SQLServerDriver",
    #     "connection.connectionString": "jdbc:sqlserver://zdwechat.cloudapp.net;databaseName=HeroStorev1;user=wechatuser;password=Server2013*?",
    #     "connection.username": "wechatuser",
    #     "connection.password": "Server2013*?"        
    # }
    # sqoop.create_connection(name="zdwechat message",
    #                         framework_params=fw_ps,
    #                         connector_params=co_ps)
    
if __name__ == "__main__":
    main()
