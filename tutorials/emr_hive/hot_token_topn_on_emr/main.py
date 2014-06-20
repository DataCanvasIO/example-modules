#!/usr/bin/env python
# -*- coding: utf-8 -*-

from specparser import EmrHiveRuntime

def main():
    hr = EmrHiveRuntime()
    hr.execute("main.hql")
    print("Done")

if __name__ == "__main__":
    main()