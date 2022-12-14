#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Author: Martin Dagleish (MRJD)

Version 0.3.3

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

# * Changelog:
# * 0.3.3 - Fixed regex pattern for rare cases where there is nothing after last z-coordinate.
# * 0.3.2 - Fixed the replace implementation and move old_std when new is created.
# * 0.3.1 - Fixed bug for coordinates with double digits
# * 0.3.0 - Simplified the code (unnecessary if statements removed) and prettified the print statements.
# * 0.2.0 - Added fix for negative values for the number of atoms and renewed the regex pattern.
# * 0.1.0 - Initial release

import os
import sys

try:
    import re
except ImportError:
    print("Please install re. (regular expressions for Python)")
    sys.exit(1)

#! https://regex101.com/r/1U1YsC/1 -> updated Regex Pattern
pattern = r"\b\w{1,2}\s+((\-|\+)?\d+[,.]\d+\s*){3,3}"  # * independent of \n

# * Old patterns:
# lp_pattern = r"\bLp\s+((-| )\d[,.]\d+\s+){3,3}" # ! match the pattern for Lp -> https://regex101.com/r/Wt0mek/1
regex = re.compile(pattern)
VERSION = "0.3.3"

def main():
    """
    Main function for running the script.
    """
    counter = 0

    for file_w_ext in files:

        filename, ext = os.path.splitext(file_w_ext)
        new_filename = filename + "_std" + ext

        with open(file_w_ext, "r", encoding="utf-8") as f:
            lines = f.readlines()  # * read all lines
            lp_count = sum(
                "Lp" in line for line in lines
            )  # * count the number of Lp lines
            xx_count = sum("Xx" in line for line in lines)
            if int(lines[0]) < 0:
                print(
                    "Error: Number of atoms is negative. -> Going to use absolute value."
                )
                lines[0] = str(abs(int(lines[0])))
            num_atoms = str(int(lines[0]) - lp_count - xx_count)  # * number of atoms
        with open(
            new_filename, "w", encoding="utf-8"
        ) as f:
            f.write(num_atoms + "\n")  # * write the number of atoms
            f.write("\n")  # * write a blank line
            for line in lines:
                match = re.search(regex, line)
                if match:
                    match = match.group(0).strip()

                    if "Lp" in line:
                        continue

                    f.write(match + "\n")

        print(
            f"\n  Export of {filename + ext} as {new_filename} finished."
        )
        counter += 1
        print(f"  {counter} / {len(files)} files exported.")


if __name__ == "__main__":
    choice = input("1) Run on local .xyz files 2) Specified .xyz file: ")
    if choice == "1":
        while True:
            replace_bool = input(
                "Do you want to replace exisiting converted files? (y/n) "
            )
            if replace_bool == "y":
                files = [
                    f if "std" not in f else os.remove(f)
                    for f in os.listdir(".")
                    if os.path.isfile(f)
                    and f.endswith(".xyz")
                    and not "xtbopt" in os.path.splitext(f)[0]
                ]

                files = [f for f in files if f != None]

                break
            if replace_bool == "n":
                files = [
                    f
                    for f in os.listdir(".")
                    if os.path.isfile(f)
                    and f.endswith(".xyz")
                    and not "xtbopt" in os.path.splitext(f)[0]
                    and not "std" in os.path.splitext(f)[0]
                ]  # * makes sure that files that have been changed do not get added again

                std_files = [
                    f for f in os.listdir(".") if "std" in f and f.endswith(".xyz")
                ]

                for f in std_files:
                    os.rename(f, os.path.splitext(f)[0] + "_old.xyz")

                break
            else:
                print("Pls enter a valid option. (y/n)")
        main()

    elif choice == "2":
        while True:
            user_inp = input("Enter .xyz file: ")
            if not os.path.isfile(user_inp):
                print("File not found. Try again!")
            else:
                break  # * break out of while loop
        files = [user_inp]
        main()

    print("\n\n*" + 10 * "-" + " EXPORT DONE! " + 10 * "-" + "*")
