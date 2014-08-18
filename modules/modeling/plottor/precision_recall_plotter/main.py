#!/usr/bin/env python
# -*- coding: utf-8 -*-

from specparser import get_settings_from_file

import matplotlib
matplotlib.use('Agg')

from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
import math



def drawPrecisionRecall(P, R, output_file):
    pdf = PdfPages(output_file)
    plt.figure(figsize=(8.27, 11.69), dpi=100)
    plt.plot(R, P, 'r-o')
    plt.title('Precision/Recall', fontsize = 20)
    plt.xlim(0, 1.0)
    plt.ylim(0, 1.0)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.xlabel('Recall', fontsize = 20)
    plt.ylabel('Precision', fontsize = 20)
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

    conclusion = readcolumn(settings.Input.conclusion)   
    label = readcolumn(settings.Input.label)

    precision_list = []
    recall_list = []

    hits = 0
    
    if(math.fabs(len(label)-len(conclusion)) > 1):
        raise Exception("The conclusion size is different from the label size. Can not plot. Check input please.")
    
    if(len(label) - len(conclusion) == 1 ): #label file got a header on the top
        label = label[1:]
        print "There is a header on your label csv file."
    if(len(conclusion) - len(label) == 1 ): #conculsion may got a header on the top
        conclusion = conclusion[1:]
        print "There is a header on your conclusion csv file."
   
    for i in range(len(label)):
        if conclusion[i] == label[i]:
            hits+=1
            precision_list.append(1.0*hits/(i+1))
            recall_list.append(1.0*hits/(len(label)))

    drawPrecisionRecall(precision_list,recall_list,settings.Output.report)

    print("Done")

if __name__ == "__main__":
    main()
