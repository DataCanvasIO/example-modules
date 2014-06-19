#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
from specparser import get_settings_from_file
from pprint import pprint

from sklearn import linear_model
import numpy as np
from sklearn.externals import joblib

def main():
    settings = get_settings_from_file("spec.json")
    print(settings)
    X = np.genfromtxt(settings.Input.X, delimiter=',', skip_header=1)
    lr = joblib.load(settings.Input.MODEL)
    Y_out = lr.predict(X)
    np.savetxt(settings.Output.Y, Y_out, fmt="%d", delimiter=",")
    print("Done")

if __name__ == "__main__":
    main()

