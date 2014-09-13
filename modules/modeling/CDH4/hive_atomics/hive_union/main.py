#!/usr/bin/env python
# -*- coding: utf-8 -*-

from specparser import HiveRuntime
import pyhs2
import os
from specparser import get_settings_from_file

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
    a_select_item = []
    for row in cur.fetch():
       a_schema.append(row[0])
       a_select_item.append(("%s AS %s") %(row[0],row[0]))
    query_sql = "DESCRIBE    %s" % settings.Input.table_b.val
    cur = conn.cursor()
    cur.execute(query_sql)

    b_select_item = []
    i = 0
    for row in cur.fetch():
       if(i >= len(a_schema)):
           raise Exception("The two table to be unioned have different column numbers")
       b_select_item.append(("%s AS %s")%(row[0],a_schema[i]))
       i = i+1

    if(i != len(a_schema)):
        raise Exception("The two table to be unioned have different column numbers")
    cur.close()
    conn.close()
    return [a_select_item,b_select_item]

def write_Main_hql(select_items):
    with open("main.hql","w") as file :
        file.write(
"""
DROP TABLE IF EXISTS ${OUTPUT_union_table};

CREATE TABLE ${OUTPUT_union_table} AS
SELECT *
FROM (
  SELECT %s
  FROM ${INPUT_table_a}
  UNION ALL
  SELECT %s
  FROM ${INPUT_table_b}
) unionResult;

""" %(','.join(select_items[0]),','.join(select_items[1]))
)
def main():
    hr = HiveRuntime()
    select_items = getSchema()
    write_Main_hql(select_items)
    hr.execute("main.hql")
    print("Done")

if __name__ == "__main__":
    main()
