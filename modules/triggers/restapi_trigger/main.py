#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests, json
from specparser import get_settings_from_file

def handler(uri,method):
    if method == "GET":
        r = requests.get(uri)
    elif method == "POST":
        r = requests.post(uri)
    else:
        print "Except \'GET\' and \'POST\' method, others are not supported currently"
        return
    print str(r.headers).encode("utf-8")
    print r.text.encode("utf-8")
    

def main():
    settings = get_settings_from_file("spec.json")
    print(settings)
    handler(settings.Param.uri,settings.Param.method)

    print("Done")

if __name__ == "__main__":
    main()
