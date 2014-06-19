#!/usr/bin/env python
# -*- coding: utf-8 -*-

from specparser import get_settings_from_file
import os,urllib2
from pprint import pprint

if __name__ == "__main__":
    settings = get_settings_from_file("spec.json")
    print(settings)
    with open(settings.Output.O, "w") as f:
        page=urllib2.urlopen(settings.Param.URI)
        f.write(page.read())
    print("Done")

