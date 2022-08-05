#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: Martin Dagleish

Version 0.1

This script filters all .csv files in the current dir, 
that were obtained by using a Agilent Cary 60 UV Vis Spectrometre. 
Those .csv files tend to be very long and result in unnecassary
columns which is why I wrote this script. 

MIT License

Copyright (c) 2022 Martin Dagleish

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import os
import re

#! https://regex101.com/r/WivPsO/1
# pattern_1 = r"\w+\:\s(-\d+\.\d+)\s\w+\:\s\d\.\d+\s\w+\:\s\d\.\d\.\d\s\(\w+\)"
# pattern_2 = r"\b\w\s+((-| )\d[,.]\d+\s+){3,3}"
# regex_1 = re.compile(pattern_1)
# regex_2 = re.compile(pattern_2)

# test_str = """
#            -------------------------------------------------
#           |               Frequency Printout                |
#            -------------------------------------------------
#  projected vibrational frequencies (cm⁻¹)
# eigval :       -0.00    -0.00    -0.00    -0.00     0.00     0.00
# eigval :      -55.23    84.15   111.83   334.55   515.01   536.31
# eigval :      640.65   722.05   740.31   783.13   857.82  1308.47
# eigval :     1393.02  1907.54  2034.95
#  reduced masses (amu)
#    1: 15.74   2: 15.76   3: 15.59   4: 15.60   5: 15.53   6: 15.55   7: 15.96   8: 16.00
#    9: 15.82  10: 15.34  11: 15.56  12: 15.71  13: 15.26  14: 15.49  15: 14.51  16: 15.04
#   17: 15.06  18: 15.72  19: 15.45  20: 14.68  21: 14.67
#  IR intensities (km·mol⁻¹)
#    1:  0.07   2:  0.08   3:  0.07   4:  0.16   5:  0.06   6:  0.08   7:  0.22   8:  0.05
#    9:  8.63  10:494.66  11:583.54  12: 85.96  13:126.80  14:192.93  15: 88.65  16:  9.51
#   17:191.97  18:442.66  19:112.16  20:625.02  21:712.82
#  Raman intensities (amu)
#    1:  0.00   2:  0.00   3:  0.00   4:  0.00   5:  0.00   6:  0.00   7:  0.00   8:  0.00
#    9:  0.00  10:  0.00  11:  0.00  12:  0.00  13:  0.00  14:  0.00  15:  0.00  16:  0.00
#   17:  0.00  18:  0.00  19:  0.00  20:  0.00  21:  0.00
# """


#! https://regex101.com/r/wKXoVG/1
pattern_1 = r"eigval\s:\s+ (( |-)\d+\.\d+\s+){1,}"
regex_1 = re.compile(pattern_1)

def main():
    for file in files:
        with open(file, "r", encoding="utf-8") as f:
            lines = f.readlines()
        with open(os.path.splitext(file)[0] + "_chemcraft.xyz", "w", encoding="utf-8") as f:
            counter = 0
            for line in lines:
                match_1 = regex_1.search(line)
                if match_1:
                    f.write(match_1.group(0) + "\n")
                    counter += 1
                # if "eigenval" in line: 

                # match_2 = re.search(regex_1, line) # search checks anywhere in string, match only checks beginning
                # match_3 = re.search(regex_2, line) # https://docs.python.org/3/library/re.html#search-vs-match 
                # if num_atoms in line:
                #     f.write(line)
                # elif match_2: 
                #     f.write(match_2.group(1) + "\t frame " + str(counter) + "\txyz file by xtb" + "\n")
                #     counter += 1
                # elif match_3: 
                #     f.write(line)

if __name__ == "__main__":
    choice = input("1) Run on local .xyz files 2) Specified .xyz file: ")
    if choice == "1":
        files = [f for f in os.listdir(".") if os.path.isfile(f) and f.endswith(".xyz")]
        main() 

    elif choice == "2":
        while True:
            filename = input("Enter .xyz file: ")
            if os.path.isfile(filename):
                break
            else:
                print("File not found.")
        files = [filename]
        main()





