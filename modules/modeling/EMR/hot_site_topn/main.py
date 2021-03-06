#!/usr/bin/env python
# -*- coding: utf-8 -*-

from specparser import EmrPigRuntime


def main():

    emr_pig_runtime = EmrPigRuntime()
    emr_pig_runtime.execute("main.pig")

    print("Done")

if __name__ == "__main__":
    main()