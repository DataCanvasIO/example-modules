#!/usr/bin/env python
# -*- coding: utf-8 -*-

from specparser import get_settings_from_file

def ReadMatrix(filePath, delimiter, skip_header):
    f = file(filePath)
    for i in range(skip_header):
        f.readline()
    matrix = []
    for line in f.readlines():
        line = line.strip()
        matrix.append(line.split(delimiter))
    return matrix

def main():
    settings = get_settings_from_file("spec.json")
    print(settings)

    # Read Matrix here
    m1 = ReadMatrix(settings.Input.File1, ',', 1)
    m2 = ReadMatrix(settings.Input.File2, ',', 1)

    # Get Min row of two matrix
    minx = min(len(m1),len(m2))
    
    # Compare two matrix
    same = total = 0
    for ix in range(minx):
        miny = min(len(m1[ix]),len(m2[ix]))
        for iy in range(miny):
            if m1[ix][iy] == m2[ix][iy]:
                same += 1
            total += 1
    
    f = open(settings.Output.Result, 'w')
    f.write('%.2f%%' % (float(same)/total*100))
    f.flush()
    f.close()

    print("Done")

if __name__ == "__main__":
    main()
