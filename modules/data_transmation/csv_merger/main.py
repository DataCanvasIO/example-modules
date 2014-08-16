#!/usr/bin/env python
# -*- coding: utf-8 -*-

from specparser import get_settings_from_file
import csv


def sniff_csv(csvfile):
    csv_sniffer = csv.Sniffer()
    buf = csvfile.read(1024)
    dialect = csv_sniffer.sniff(buf)
    has_header = csv_sniffer.has_header(buf)
    csvfile.seek(0)
    return dialect, has_header

def make_header(num):
    header = []
    for i in range(num):
      header.append('c'+str(i))
    return header

def get_header_data(filename):
    try:
        with open(filename, "rb") as f:
            dialect, has_header = sniff_csv(f)
            data = list(csv.reader(f, dialect))
            if has_header:
                data_header = data[0]
                data = data[1:]
                return True,data_header,data
            else:
                return False,None,data
    except:
        with open(filename,"rb") as f:
            data_header_len = 0
            data = []
            while 1:
                line = f.readline()
                if not line :
                    break 
                data_header_len=len(line.split(','))
                data.append(line.rstrip('\n').split(','))
            return False,None,data


def main():
    settings = get_settings_from_file("spec.json")
    print(settings)

    # TODO: Add your code here
        
    left_part = get_header_data(settings.Input.x)
    right_part = get_header_data(settings.Input.y)
    
    file_merged = open(settings.Output.merged_file,"wb")
    writer = csv.writer(file_merged)

    if(left_part[0] and right_part[0] ):
        left_part[1].extend(right_part[1])
        writer.writerow(left_part[1])
    if(len(left_part[2]) != len(right_part[2])):
        raise Exception
     
    
    for i in range(len(left_part[2])):
        l = left_part[2][i]
        r = right_part[2][i]   
        l.extend(r)
        writer.writerow(l)
    file_merged.close()
      

    
    print("Done")

if __name__ == "__main__":
    main()
