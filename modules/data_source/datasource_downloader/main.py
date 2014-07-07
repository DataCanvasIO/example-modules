#!/usr/bin/env python
# -*- coding: utf-8 -*-

from specparser import get_settings_from_file
import urllib
import json

def main():
    settings = get_settings_from_file("spec.json")
    print(settings)

    # TODO: Add your code here
    with open(settings.Input.DS) as f:
        ds = json.load(f)
        print("Downloading '%s'..." % settings.Input.DS)
        urllib.urlretrieve(ds['URL'], filename=settings.Output.O)

    print("Done")

if __name__ == "__main__":
    main()