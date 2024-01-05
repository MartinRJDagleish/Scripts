#!/usr/bin/env python3
# ------------------------------------------------------------------
#
# Script for creating input files for ionization potential omega tuning
#
# To use execute with the filename as the output with both files in the same location
#
# The input format is:
#                  'python make_input_files min max step'
#
# An example is:
#                  'python make_input_files 100 200 20'
#
# ------------------------------------------------------------------
# ==================================================================
# Written by Bradley D. Rose 11/2014
# http://www.bradleydrose.com/
# Please let me know if you have any problems using this script
# ==================================================================
# Modified by Martin Dagleish (MRJD) on 2020-08-10

import fileinput
import os
import shutil
import sys

makeList = []

lowLimit = int(sys.argv[1])
highLimit = int(sys.argv[2])
stepSize = int(sys.argv[3])

# read omega limits
for n in range(lowLimit, highLimit + 1, stepSize):
    makeList.append(n)

# make and write to new files
for n in makeList:
    shutil.copyfile("omegaIP_Value.inp", "omegaIP_{0}.inp".format(n))
    f = open("omegaIP_{0}.inp".format(n), "r")
    filedata = f.read()
    f.close()

    newdata = filedata.replace("Value", "{0}".format(n))

    f = open("omegaIP_{0}.inp".format(n), "w")
    f.write(newdata)
    f.close()
