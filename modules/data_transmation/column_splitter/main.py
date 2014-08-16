#!/usr/bin/env python
# -*- coding: utf-8 -*-

from specparser import get_settings_from_file
import csv


def main():
    settings = get_settings_from_file("spec.json")
    print(settings)

    # TODO: Add your code here
    
    pivot = int(settings.Param.split_index)
    
    foutput1 = open(settings.Output.output1,"wb")
    foutput2 = open(settings.Output.output2,"wb")
    
    output1_writer = csv.writer(foutput1,lineterminator='\n')
    output2_writer = csv.writer(foutput2,lineterminator='\n')



    with open(settings.Input.input_file,"r") as fin:
        while 1:
            line = fin.readline()
            if not line:
                break
            columns = line.rstrip('\n').split(',')
            output1_writer.writerow(columns[:pivot])
            output2_writer.writerow(columns[pivot:])        
    
    foutput1.close()
    foutput2.close()
    fin.close()
    print("Done")

if __name__ == "__main__":
    main()
