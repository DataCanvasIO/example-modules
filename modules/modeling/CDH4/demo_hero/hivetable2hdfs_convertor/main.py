#!/usr/bin/env python
# -*- coding: utf-8 -*-

from specparser import get_settings_from_file
from pprint import pprint
import pyhs2
#import csv

if __name__ == "__main__":
    settings = get_settings_from_file("spec.json")
    print(settings)

    conn = pyhs2.connect(host=settings.Param.HiveServer2_Host,
            port=int(settings.Param.HiveServer2_Port),
            authMechanism="PLAIN",
            user="hive",
            password="",
            database="default")
    query_sql = "DESCRIBE FORMATTED   %s" % settings.Input.table_name.val
    cur = conn.cursor()
    cur.execute(query_sql)

    with open(settings.Output.output_dir, 'wb') as file:
            # print header
            for row in cur.fetch():
		if row[0].strip(" ") == "Location:":
                	file.write(row[1])
    
    cur.close()
    conn.close()
