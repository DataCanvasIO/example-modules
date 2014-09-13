#!/usr/bin/env python
# -*- coding: utf-8 -*-

from specparser import HiveRuntime
from specparser import get_settings_from_file

def write_Main_hql():
    settings = get_settings_from_file("spec.json")
    limit_string = ""
    if(settings.Param.limit is not None and settings.Param.limit.strip(' ') != ''):
        limit_string = "limit "+settings.Param.limit
    with open("main.hql","w") as file:
        file.write(
"""
DROP TABLE IF EXISTS ${OUTPUT_ordered_table};

CREATE TABLE ${OUTPUT_ordered_table} AS
SELECT *
FROM ${INPUT_from_table}
ORDER BY ${PARAM_order_by_columns} %s 
;
 
""" % limit_string
)

def main():
    hr = HiveRuntime()
    write_Main_hql()
    hr.execute("main.hql")
    print("Done")

if __name__ == "__main__":
    main()
