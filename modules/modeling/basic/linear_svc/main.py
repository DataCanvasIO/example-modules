#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
from specparser import get_settings_from_file
from pprint import pprint

from sklearn.svm import LinearSVC
import numpy as np
from sklearn.externals import joblib
import pickle

def main():
    settings = get_settings_from_file("spec.json")
    print(settings)
    X = np.genfromtxt(settings.Input.X, delimiter=',', skip_header=1)
    Y = np.genfromtxt(settings.Input.Y, delimiter=',', skip_header=1)
    svc = LinearSVC(C=float(settings.Param.C), loss=settings.Param.loss, penalty=settings.Param.penalty)
    svc.fit(X,Y)
    # joblib.dump(svc, settings.Output.MODEL, cache_size=1e9)
    with open(settings.Output.MODEL, "w") as f:
        pickle.dump(svc, f)
    print("Done")

if __name__ == "__main__":
    main()

