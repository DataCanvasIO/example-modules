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
__version__ = "0.0.2"
__author__ = "xiaolin"

import requests
import json
import copy
import urllib
import re
import time

def current_milli_time():
    return int(round(time.time() * 1000))

class MySqoop(object):
    def __init__(self, host, port):
        self._svc_root = "http://%s:%s/sqoop" % (host, port)

    def version(self):
        return requests.get(self._svc_root + "/version").json()

    def framework(self):
        return requests.get(self._svc_root + "/v1/framework").json()

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

    def get_connection_inputs(self, connection_name):
        connection = self.get_connection_by_name(connection_name)
        input_dict = {
            c['name']:urllib.unquote(c["value"])
            for c in connection['connector'][0]['inputs']
            if "value" in c
        }
        return input_dict

    def _create_connection(self, name, framework_params, connector_params):
        r = self.framework()
        framework_import_form = copy.deepcopy(r['con-forms'])
        for f in framework_import_form:
            for fi in f['inputs']:
                if fi['name'] in framework_params:
                    fi['value'] = urllib.quote(framework_params[fi['name']], '')

        connector = self.connector()['all'][0]
        connector_forms = copy.deepcopy(connector['con-forms'])
        # pp(connector_forms)
        for c in connector_forms:
            for ci in c['inputs']:
                if ci['name'] in connector_params:
                    ci['value'] = urllib.quote(connector_params[ci['name']], '')

        now_time = current_milli_time()
        new_d = {
            "id": -1,
            "enabled": True,
            "update-date": now_time,
            "creation-date": now_time,
            "name": name,
            "connector": connector_forms,
            "connector-id": connector['id'],
            "framework": framework_import_form,
            "update-user": None,
            "creation-user" : "xiaolin"
        }
        all_d = { "all": [ new_d ] }
        print("=====================")
        pp(all_d)
        print("=====================")
        r = requests.post(self._svc_root + "/v1/connection", data=json.dumps(all_d), headers={'content-type': 'application/json'})
        if r.status_code != 200:
            print("--------------------")
            pp(all_d)
            pp(r.status_code)
            pp(r.json())
            raise Exception("Failed to create a connection")
        else:
            return r.json()

    def create_connection(self, conn_name, conn_str, username, password):
        jdbc_cfg = parse_jdbc(conn_str)

        jdbc_driver_dict = {
                "sqlserver" : "com.microsoft.sqlserver.jdbc.SQLServerDriver",
                "postgresql" : "org.postgresql.Driver"
        }
        if not jdbc_cfg['name'] in jdbc_driver_dict:
            raise ValueError("Do not support jdbc driver '%s'" % jdbc_cfg['name'])

        fw_ps = { }
        co_ps = {
                "connection.jdbcDriver": jdbc_driver_dict[jdbc_cfg['name']],
                "connection.connectionString": conn_str,
                "connection.username": username,
                "connection.password": password
        }

        return self._create_connection(conn_name, fw_ps, co_ps)

    def delete_connection_by_id(self, cid):
        print "Delete connection %d" % int(cid)
        return requests.delete(self._svc_root + "/v1/connection/%d" % int(cid)).json()

    def get_job(self, jid=None):
        if not jid:
            return requests.get(self._svc_root + "/v1/job/all").json()
        else:
            return requests.get(self._svc_root + "/v1/job/" + str(jid)).json()

    def create_job(self, job_name, connection, framework_params, job_params, job_type):
        if not job_type.upper() in ["IMPORT", "EXPORT"]:
            raise ValueError("Invalid type job type")

        job_type = job_type.upper()

        r = self.framework()
        framework_form = copy.deepcopy(r['job-forms'][job_type])
        for f in framework_form:
            for fi in f['inputs']:
                if fi['name'] in framework_params:
                    fi['value'] = urllib.quote(framework_params[fi['name']], '')

        connector = self.connector(connection['connector'][0]['id'])
        connector_job_form = copy.deepcopy(connector['all'][0]['job-forms'][job_type])
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
            "framework": framework_form,
            "id": -1,
            "name": job_name,
            "type": job_type,
            "update-date": now_time,
            "update-user": None
        }

        all_d = { "all":[ new_d ] }
        r = requests.post(self._svc_root + "/v1/job", data=json.dumps(all_d), headers={'content-type': 'application/json'})
        if r.status_code != 200:
            pp(all_d)
            raise Exception("Failed to create a '%s' job" % job_type)
        else:
            return r.json()

    def create_import_job(self, job_name, connection_id, framework_params, job_params):
        connection = self.connection(connection_id)['all'][0]
        return self.create_job(job_name, connection, framework_params, job_params, job_type="IMPORT")

    def create_export_job(self, job_name, connection_id, framework_params, job_params):
        connection = self.connection(connection_id)['all'][0]
        return self.create_job(job_name, connection, framework_params, job_params, job_type="EXPORT")

    def delete_job(self, jid):
        r = requests.delete(self._svc_root + "/v1/job/" + str(jid))
        if r.status_code != 200:
            raise Exception("Failed to delete a job: '%s', status_code=%s" % (str(jid), r.status_code))
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

            ret = r.json()
            print("Job status '%s'" % ret['all'][0]['status'])
            if ret['all'][0]['status'] in ['FAILURE_ON_SUBMIT']:
                raise Exception("Failed to run a job: '%s'" % str(jid))

            if ret['all'][0]['status'] in ['SUCCEEDED', 'UNKNOWN', 'FAILED']:
                return r

def pp(j):
    print(json.dumps(j, indent=4, sort_keys=True))

def parse_jdbc(name):
    pattern = re.compile(r'''
            jdbc:
            (?P<name>[\w\+]+)://
            (?:
                (?P<username>[^:/]*)
                (?::(?P<password>.*))?
            @)?
            (?:
                (?:
                    \[(?P<ipv6host>[^/]+)\] |
                    (?P<ipv4host>[^/:;]+)
                )?
                (?::(?P<port>[^/]*))?
            )?
            (?:/(?P<database>[^;]*))?
            (?P<meta_params>;.*)?
    ''', re.X)

    meta_pattern = re.compile(r'''
            (?P<key>[^=;]+)=(?P<val>[^=;]+)
    ''', re.VERBOSE)

    m = pattern.match(name)
    if m is not None:
        ret = m.groupdict()
        if m.group("meta_params"):
            metas = meta_pattern.findall(m.group("meta_params"))
            ret['meta'] = {k:v for k,v in metas}
        return ret
    else:
        raise ValueError("Invalid jdbc string")

def pymssql_delete_table(cfg, tablename):
    import pymssql
    server = cfg['ipv4host']
    def get_username(cfg):
        username = cfg.get('username', None)
        if username:
            return username

        if 'meta' not in cfg:
            return None

        return cfg['meta'].get('user', None)

    def get_password(cfg):
        password = cfg.get('password', None)
        if password:
            return password

        if 'meta' not in cfg:
            return None

        return cfg['meta'].get('password', None)

    user = get_username(cfg)
    password = get_password(cfg)
    dbname = cfg['meta']['databaseName']   
    conn = pymssql.connect(server, user, password, dbname, tablename)
    cursor = conn.cursor()
    # TODO:
    cursor.execute("DELETE FROM %s" % tablename)
    conn.commit()

def psycopg2_delete_table(cfg,tablename):
    import psycopg2
    def get_prostegres_connection(servername,username,password_string,dbname):
        conn = psycopg2.connect("dbname='%s' user='%s' host='%s' password='%s'" %(dbname,username,servername,password_string ) )
        return conn

    def delete_data_table(post_conn,table_name):
        pos_cursor =  pos_conn.cursor()
        pos_cursor.execute("delete from %s where 1=1" % table_name)
        pos_conn.commit()

    def get_username(cfg):
        username = cfg.get('username', None)
        if username:
            return username

        if 'meta' not in cfg:
            return None

        return cfg['meta'].get('user', None)

    def get_password(cfg):
        password = cfg.get('password', None)
        if password:
            return password

        if 'meta' not in cfg:
            return None

        return cfg['meta'].get('password', None)

    server = cfg['ipv4host']
    user = get_username(cfg)
    password = get_password(cfg)
    dbname = cfg['database']   
    pos_conn = get_prostegres_connection(server,user,password,dbname)

    delete_data_table(pos_conn,tablename)

if __name__ == "__main__":
    main()
