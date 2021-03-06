#!/usr/bin/env python
# -*- coding: utf-8 -*-


from datacanvas.new_runtime import DataCanvas
dc = DataCanvas(__name__)


@dc.hadoop_runtime(spec_json="spec.json")
def mymodule(rt, params, inputs, outputs):

    rt.execute_hive_filename("main.hql")

    print("Done")


if __name__ == "__main__":
    dc.run()
