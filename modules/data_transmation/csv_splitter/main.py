#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import math 
import csv
from specparser import get_settings_from_file


def sniff_csv(csvfile):
    csv_sniffer = csv.Sniffer()
    buf = csvfile.read(1024)
    dialect = csv_sniffer.sniff(buf)
    has_header = csv_sniffer.has_header(buf)
    csvfile.seek(0)
    return dialect, has_header

def main():
    settings = get_settings_from_file("spec.json")
    print(settings)

    with open(settings.Input.input_file, "rb") as f:
        dialect, has_header = sniff_csv(f)
        data = list(csv.reader(f, dialect))
	if has_header:
            data_header = data[0]
            data = data[1:]

    if int(settings.Param.random_seed) > 0 :
        random.seed(int(settings.Param.random_seed))
    else:
        random.seed(None)
        
    random.shuffle(data)
    # data = [i for i in data if i != '']
    total = len(data)
    pivot = int(math.floor(total*float(settings.Param.train_ratio)))
    train_data = data[:pivot]
    test_data = data[pivot:] 
    with open(settings.Output.train_file,"w") as train_f:
        train_writer = csv.writer(train_f,lineterminator='\n')
        if has_header:
            train_writer.writerow(data_header)
        for val in train_data:
            train_writer.writerow(val)
      
    with open(settings.Output.test_file,"w") as test_f:
        test_writer = csv.writer(test_f,lineterminator='\n')
        if has_header:
            test_writer.writerow(data_header)
        for val in test_data:
            test_writer.writerow(val)
    
    f.close()
    train_f.close()
    test_f.close()
    print("Done")

if __name__ == "__main__":
    main()
