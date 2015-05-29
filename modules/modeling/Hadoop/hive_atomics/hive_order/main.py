#!/usr/bin/env python
# -*- coding: utf-8 -*-


from datacanvas.new_runtime import DataCanvas
dc = DataCanvas(__name__)

def write_main_hql(params):
    limit_string = ""
    if(params.limit is not None and params.limit.strip(' ') != ''):
        limit_string = "limit "+ params.limit
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

@dc.hadoop_runtime(spec_json="spec.json")
def mymodule(rt, params, inputs, outputs):
    
    write_main_hql(params)

    rt.execute_hive_filename("main.hql")

    print("Done")


if __name__ == "__main__":
    dc.run()
