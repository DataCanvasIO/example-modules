#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
from specparser import get_settings_from_file
from pprint import pprint

from sklearn import linear_model
import numpy as np
from sklearn.externals import joblib
import pickle

def main():
    settings = get_settings_from_file("spec.json")
    print(settings)
    X = np.genfromtxt(settings.Input.X, delimiter=',', skip_header=1)
    Y = np.genfromtxt(settings.Input.Y, delimiter=',', skip_header=1)
    lr = linear_model.LogisticRegression(C=float(settings.Param.C), penalty=settings.Param.penalty)
    lr.fit(X,Y)
    # joblib.dump(lr, settings.Output.MODEL, compress=9, cache_size=1e9)
    with open(settings.Output.MODEL, "w") as f:
        pickle.dump(lr, f)
    print("Done")

if __name__ == "__main__":
    main()

