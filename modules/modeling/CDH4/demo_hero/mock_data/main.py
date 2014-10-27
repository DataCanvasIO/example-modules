#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from specparser import HadoopRuntime


def main():
    hr = HadoopRuntime()
    settings = hr.settings
    settings.Output.hdfs_path.val = settings.Param.data_path

    print("Done")

if __name__ == "__main__":
    main()
