#!/usr/bin/env python
# -*- coding: utf-8 -*-

from specparser import HiveRuntime

def main():
    hr = HiveRuntime()
    hr.execute("main.hql")
    hr.settings.Output.output_table2.val = hr.settings.Output.output_table1.val
    print("Done")

if __name__ == "__main__":
    main()
