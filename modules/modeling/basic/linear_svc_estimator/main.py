#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
from specparser import get_settings_from_file
from pprint import pprint
import csv
from sklearn.svm import LinearSVC
import numpy as np
from sklearn.externals import joblib

import matplotlib
matplotlib.use('Agg')
 
import datetime
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt

def drawPrecisionRecall(X,Y,output_file):
    pdf = PdfPages(output_file) 
    plt.figure(figsize=(len(Y), len(X))) 
    plt.plot(Y, X, 'r-o') 
    plt.title('Precision/Recall') 
    pdf.savefig()  # saves the current figure into a pdf page 
    plt.close() 
    pdf.close()

def readcolumn(filename):
    column = []
    with open(filename,"r") as fconcl:
        for line in fconcl:
            column.append(line.rstrip('\n'))
    return  column

def main():
    settings = get_settings_from_file("spec.json")
    print(settings)
    X = np.genfromtxt(settings.Input.X, delimiter=',', skip_header=1)
    svc = joblib.load(settings.Input.MODEL)
    Y_out = svc.predict(X)
    Y_list = [Y_out]
    np.savetxt("./conclusion.csv", Y_out, fmt="%d", delimiter=",")
    
    conclusion = readcolumn("./conclusion.csv")
    label = readcolumn(settings.Input.Y) 
 
    precision_list = []
    recall_list = []
    
    hits = 0
    for i in range(len(label)):
        if conclusion[i] == label[i]:
            hits+=1
            precision_list.append(1.0*hits/(i+1)) 
            recall_list.append(1.0*hits/(len(label)))

    drawPrecisionRecall(precision_list,recall_list,settings.Output.report)
    print("Done")


if __name__ == "__main__":
    main()
