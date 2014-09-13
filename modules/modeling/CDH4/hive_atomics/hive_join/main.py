#!/usr/bin/env python
# -*- coding: utf-8 -*-

from specparser import get_settings_from_file
from pprint import pprint
import pyhs2
from specparser import HiveRuntime
import os

def getSchema():
    settings = get_settings_from_file("spec.json")
    print(settings)

    conn = pyhs2.connect(host=settings.Param.HiveServer2_Host,
            port=int(settings.Param.HiveServer2_Port),
            authMechanism="PLAIN",
            user="hive",
            password="",
            database="default")
    query_sql = "DESCRIBE    %s" % settings.Input.table_a.val
    cur = conn.cursor()
    cur.execute(query_sql)

    a_schema = []
    for row in cur.fetch():
       a_schema.append(("a.%s AS a_%s") %(row[0],row[0]))
  
    query_sql = "DESCRIBE    %s" % settings.Input.table_b.val
    cur = conn.cursor()
    cur.execute(query_sql)

    b_schema = []
    for row in cur.fetch():
       b_schema.append(("b.%s AS b_%s")%(row[0],row[0]))
             
    cur.close()
    conn.close()
    return [a_schema,b_schema]

def write_Main_hql(columns):
    settings = get_settings_from_file("spec.json")

    with open("main.hql","w") as file:
        file.write(
"""
DROP TABLE IF EXISTS ${OUTPUT_joined_table};
CREATE TABLE ${OUTPUT_joined_table} AS
SELECT %s 
FROM ${INPUT_table_a} a %s JOIN ${INPUT_table_b} b 
ON %s 
;
""" %(columns,settings.Param.join_type,settings.Param.on_condition) )

def main():
    hr = HiveRuntime()
    s = getSchema()
    schema_a = ",".join(s[0])
    schema_b = ",".join(s[1])
    columns =  ",".join((schema_a,schema_b))
    write_Main_hql(columns)
#   print ",".join(s[1])
    hr.execute("main.hql")
    print("Done")

if __name__ == "__main__":
    main()
