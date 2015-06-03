#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datacanvas.new_runtime import GenericHadoopRuntime, DataCanvas
from datacanvas.io_types import DS_HDFS
import shlex


dc = DataCanvas(__name__)


@dc.hadoop_runtime(spec_json="spec.json")
def mymodule(rt, params, inputs, outputs):

    if rt.hadoop_type not in ["CDH4", "CDH5"]:
        raise Exception("Do not support cluster type '%s'" % rt.cluster_type)
    
    # Check params
    if not params.connect_string.val.strip():
        raise ValueError("Param 'connect_string' should not be empty")

    if not params.table.val.strip():
        raise ValueError("Param 'table' should not be empty")

    # Build params for sqoop command
    additional_params = shlex.split(params.additional_params)
    sqoop_cmd = ["sqoop", "export",
                 "--connect", params.connect_string.val,
                 "--username", params.username.val,
                 "--password", params.password.val,
                 "--table", params.table.val]
    export_dir = inputs.I.val.URL

    sqoop_cmd += ["--export-dir", export_dir]

    ret = rt.cluster.hadoop_cmd(sqoop_cmd + additional_params)
    if ret:
        raise Exception("Failed to execute 'sqoop export' command")
    

if __name__ == "__main__":
    dc.run()

