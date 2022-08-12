#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: Martin Dagleish (MRJD)

Version 0.1

This script converts the Chem3D Tinker xyz files to standard xyz files.
This is needed in order to use the .xyz files for any other program.
Tinker xyz files have many useless numbers and lines that are not needed.

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
import sys

try: 
    import re 
except ImportError:
    print("Please install re. (regular expressions for Python)")
    sys.exit()

#! https://regex101.com/r/WivPsO/1
pattern = r"\b\w\s+((-| )\d[,.]\d+\s+){3,3}"  # * independent of \n
# pattern2 = r"\b\w\s+((-| )\d[,.]\d+\s+){3,3}\n" #* not working!
# lp_pattern = r"\bLp\s+((-| )\d[,.]\d+\s+){3,3}" # ! match the pattern for Lp -> https://regex101.com/r/Wt0mek/1
regex = re.compile(pattern)


def main():
    """
    Main function for running the script.
    """
    for file in files:
        with open(file, "r", encoding="utf-8") as f:
            lines = f.readlines()  # * read all lines
            lp_count = sum(
                "Lp" in line for line in lines
            )  # * count the number of Lp lines
            xx_count = sum(
                "Xx" in line for line in lines
            )
            if int(lines[0]) < 0:
                print("Error: Number of atoms is negative.")
                sys.exit(1)
            num_atoms = str(int(lines[0]) - lp_count - xx_count)  # * number of atoms
        with open(os.path.splitext(file)[0] + "_std.xyz", "w", encoding="utf-8") as f:
            f.write(num_atoms + "\n")  # * write the number of atoms
            f.write("\n")  # * write a blank line
            for line in lines:
                match = re.search(regex, line)
                if match:
                    if "Lp" in line:
                        continue
                    elif match.group(0).endswith("\n"):
                        try:
                            f.write(
                                match.group(0)
                            )  # * \n in line already -> no double newlines
                        except UnicodeEncodeError:
                            pass
                    else:
                        try:
                            f.write(match.group(0) + "\n")
                        except UnicodeEncodeError:
                            pass


if __name__ == "__main__":
    choice = input("1) Run on local .xyz files 2) Specified .xyz file: ")
    if choice == "1":
        files = [
            f
            for f in os.listdir(".")
            if os.path.isfile(f)
            and f.endswith(".xyz")
            and not os.path.splitext(f)[0].endswith("xtbopt")
            and not os.path.splitext(f)[0].endswith("_chemcraft")
            and not os.path.splitext(f)[0].endswith("_std")
        ]  # makes sure that files that have been changed do not get added again
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
