#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
from specparser import get_settings_from_file
from pprint import pprint
import pyhs2
import csv

if __name__ == "__main__":
    settings = get_settings_from_file("spec.json")
    print(settings)

    conn = pyhs2.connect(host=settings.Param.Host,
            port=int(settings.Param.Port),
            authMechanism="PLAIN",
            user="hive",
            password="",
            database="default")

    where_clause = settings.Param.Where_Clause
    schema = settings.Param.SCHEMA
    input_tbl = settings.Input.input_tbl.val
    limit = settings.Param.LIMIT
    if where_clause.strip():
        query_sql = """SELECT %s
FROM %s
WHERE %s
LIMIT %s""" % (schema, input_tbl, where_clause, limit)

    else:
        query_sql = """SELECT %s
FROM %s
LIMIT %s""" % (schema, input_tbl, limit)

    print("Query to execute:")
    print("=================")
    print(query_sql)
    print("=================")

    cur = conn.cursor()
    cur.execute(query_sql)

    with open(settings.Output.O, 'wb') as csvfile:
        # print header
        sch = cur.getSchema()
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow([s['columnName'] for s in sch])

        for row in cur.fetch():
            csvwriter.writerow([str(i) for i in row])

    cur.close()
    conn.close()

