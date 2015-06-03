#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datacanvas.new_runtime import GenericHadoopRuntime, DataCanvas
from datacanvas.io_types import DS_HDFS
import shlex


dc = DataCanvas(__name__)


@dc.hadoop_runtime(spec_json="spec.json")
def mymodule(rt, params, inputs, outputs):
    
    # Check params
    if not params.connect_string.val.strip():
        raise ValueError("Param 'connect_string' should not be empty")

    if not params.table.val.strip():
        raise ValueError("Param 'table' should not be empty")

    # Build params for sqoop command
    additional_params = shlex.split(params.additional_params)
    sqoop_cmd = ["sqoop", "import",
                 "--connect", params.connect_string.val,
                 "--username", params.username.val,
                 "--password", params.password.val,
                 "--table", params.table.val]
    target_dir = params.target_dir.val.strip()
    if not target_dir:
        target_dir = rt.get_working_dir("sqoop1_table_" + params.table.val)

    sqoop_cmd += ["--target-dir", target_dir]

    ret = rt.cluster.hadoop_cmd(sqoop_cmd + additional_params)
    if ret:
        raise Exception("Failed to execute 'sqoop import' command")

    # Write output object
    out_obj = DS_HDFS(URL=target_dir)
    outputs.O.val = out_obj
    

if __name__ == "__main__":
    dc.run()
