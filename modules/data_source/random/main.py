#!/usr/bin/env python
# -*- coding: utf-8 -*-

from specparser import get_settings_from_file

from random import random

def GetRandom(imax, intType):
    rf = random() * imax
    if intType:
        return str(int(rf))
    return str(rf)

def main():
    settings = get_settings_from_file("spec.json")
    print(settings)

    # init parameter here
    f = open(settings.Output.Matrix, 'w')
    intx = int(float(settings.Param.X))
    inty = int(float(settings.Param.Y))
    imax = int(float(settings.Param.Max))
    intType = settings.Param.Type == 'int'
    
    # write random num to file
    f.write('COLUMN_%d' % 0)
    for iy in range(inty-1):
        f.write(',COLUMN_%d' % (iy + 1))
    
    for ix in range(intx):
		f.write('\n')
		f.write(GetRandom(imax, intType))
		for iy in range(inty-1):
			f.write(',%s' % GetRandom(imax, intType))
    f.flush()
    f.close()

    print("Done")

if __name__ == "__main__":
    main()
