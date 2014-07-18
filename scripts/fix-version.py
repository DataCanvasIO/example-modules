#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
# from collections import OrderedDict

from collections import OrderedDict as _OrderedDict
try:
    from thread import get_ident as _get_ident
except ImportError:
    from dummy_thread import get_ident as _get_ident


class ListDict(_OrderedDict):
    def __init__(self, *args, **kwds):
        try:
            self.__insertions_running
        except AttributeError:
            self.__insertions_running = {}
        super(ListDict, self).__init__(*args, **kwds)

    def __setitem__(self, key, value, dict_setitem=dict.__setitem__):
        if _get_ident() in self.__insertions_running:
            self.__insertions_running[_get_ident()] = key, value
        else:
            super(ListDict, self).__setitem__(key, value, dict_setitem)

    def __insertion(self, link_prev, key_value):
        self.__insertions_running[_get_ident()] = 1
        self.__setitem__(*key_value)
        key, value = self.__insertions_running.pop(_get_ident())
        if link_prev[2] != key:
            if key in self:
                del self[key]
            link_next = link_prev[1]
            self._OrderedDict__map[key] = link_prev[1] = link_next[0] = [link_prev, link_next, key]
        dict.__setitem__(self, key, value)

    def insert_after(self, existing_key, key_value):
        self.__insertion(self._OrderedDict__map[existing_key], key_value)

    def insert_before(self, existing_key, key_value):
        self.__insertion(self._OrderedDict__map[existing_key][0], key_value)

def list_spec_json(start="."):
    for dirpath, dirnames, filenames in os.walk(start):
        for f in filenames:
            if f == "spec.json":
                yield os.path.join(dirpath, f)

def update_json(fn):
    jf = open(fn, "r")
    spec_json = json.load(jf, object_pairs_hook=ListDict)
    jf.close()

    spec_json.insert_after("Version", ("CategoryTags", []))
    for k,v in spec_json['Input'].items():
        spec_json['Input'][k] = [v]
    for k,v in spec_json['Output'].items():
        spec_json['Output'][k] = [v]

    with open(fn, "w") as sj_out:
        sj_out.write(json.dumps(spec_json, indent=4, separators=(',', ': ')))

def update_version(fn):
    jf = open(fn, "r")
    spec_json = json.load(jf, object_pairs_hook=ListDict)
    jf.close()

    try:
        v1,v2 = spec_json['Version'].split(".")
        v3 = None
    except ValueError:
        v1,v2,v3 = spec_json['Version'].split(".")

    if v3 == None:
        new_version = "%d.%d" % (int(v1), int(v2)+1)
    else:
        new_version = "%d.%d.%d" % (int(v1), int(v2), int(v3)+1)
    print(new_version)
    spec_json['Version'] = new_version

    with open(fn, "w") as sj_out:
        sj_out.write(json.dumps(spec_json, indent=4, separators=(',', ': ')))

def update_env_to_param(fn):
    jf = open(fn, "r")
    spec_json = json.load(jf, object_pairs_hook=ListDict)
    jf.close()

    spec_json.insert_after("Env", ("Param", spec_json['Env']))
    del spec_json['Env']
    print(json.dumps(spec_json, indent=4, separators=(',', ': ')))

    with open(fn, "w") as sj_out:
        sj_out.write(json.dumps(spec_json, indent=4, separators=(',', ': ')))

def capitalize_params(fn):
    jf = open(fn, "r")
    spec_json = json.load(jf, object_pairs_hook=ListDict)
    jf.close()

    # spec_json.insert_after("Env", ("Param", spec_json['Env']))
    # del spec_json['Env']
    param_dict = spec_json['Param']
    for param_key,param_val in param_dict.items():
        param_dict[param_key] = {k.capitalize():v for k,v in param_val.items()}

    print(json.dumps(spec_json, indent=4, separators=(',', ': ')))

    with open(fn, "w") as sj_out:
        sj_out.write(json.dumps(spec_json, indent=4, separators=(',', ': ')))

def check_params(fn):
    jf = open(fn, "r")
    spec_json = json.load(jf, object_pairs_hook=ListDict)
    jf.close()

    # spec_json.insert_after("Env", ("Param", spec_json['Env']))
    # del spec_json['Env']
    ret = False
    param_dict = spec_json['Param']
    for param_key,param_val in param_dict.items():
        if 'Type' not in param_val:
            ret = True

    if ret:
        print(json.dumps(spec_json, indent=4, separators=(',', ': ')))

    # with open(fn, "w") as sj_out:
    #     sj_out.write(json.dumps(spec_json, indent=4, separators=(',', ': ')))

def main():
    for f in list_spec_json("./modules/modeling/CDH4/demo_hero/"):
        print(f)
        # update_json(f)
        update_version(f)
        # update_env_to_param(f)
        # capitalize_params(f)
        # check_params(f)
    # update_json("./modules/modeling/helper/compare/spec.json")

if __name__ == "__main__":
    main()
