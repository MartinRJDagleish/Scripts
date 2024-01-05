#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Author: Martin Dagleish (MRJD)

Version 0.1.0

This script converts xyz coordinates in Bohr units to AA (Angstrom). 

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
# * 0.1.0 - Initial release

import os
import sys

try:
    import regex as re 
except ImportError:
    print("Please install regex. (regular expressions for Python)")
    sys.exit(1)

#! https://regex101.com/r/1U1YsC/1 -> updated Regex Pattern
pattern = r"\b\w{1,2}\s+((\-|\+)?\d+[,.]\d+\s*){3,3}"  # * independent of \n
regex = re.compile(pattern)
VERSION = "0.1.0"

bohr2aa = 0.529177210903

def convert_zvals_to_symbols(z_val):
    return atom_dict.get(z_val,z_val) # * If failed then return z_val (int)

atom_dict = {
        1: "H",    2: "He",
        3: "Li",   4: "Be",  5: "B",   6: "C",   7: "N",   8: "O",   9: "F",   10: "Ne",
        11: "Na", 12: "Mg", 13: "Al", 14: "Si", 15: "P",  16: "S",  17: "Cl",  18: "Ar",
        19: "K",  20: "Ca", 
            21: "Sc", 22: "Ti", 23: "V",  24: "Cr", 25: "Mn",  26: "Fe", 27: "Co", 28: "Ni", 29: "Cu", 30: "Zn", 
                            31: "Ga", 32: "Ge", 33: "As", 34: "Se", 35: "Br",  36: "Kr",
        37: "Rb", 38: "Sr", 
            39: "Y",  40: "Zr", 41: "Nb", 42: "Mo", 43: "Tc",  44: "Ru", 45: "Rh", 46: "Pd", 47: "Ag", 48: "Cd",
                            49: "In", 50: "Sn", 51: "Sb", 52: "Te", 53: "I",   54: "Xe",
        55: "Cs", 56: "Ba",
            57: "La", 58: "Ce", 59: "Pr", 60: "Nd", 61: "Pm", 62: "Sm", 63: "Eu", 64: "Gd", 65: "Tb", 66: "Dy", 67: "Ho", 68: "Er", 69: "Tm", 70: "Yb", 71: "Lu",
            72: "Hf", 73: "Ta", 74: "W",  75: "Re", 76: "Os", 77: "Ir", 78: "Pt", 79: "Au", 80: "Hg",
                            81: "Tl", 82: "Pb", 83: "Bi", 84: "Po", 85: "At", 86: "Rn",
        87: "Fr", 88: "Ra",
            89: "Ac", 90: "Th", 91: "Pa", 92: "U",  93: "Np", 94: "Pu", 95: "Am", 96: "Cm", 97: "Bk", 98: "Cf", 99: "Es", 100: "Fm", 101: "Md", 102: "No", 103: "Lr",
            104: "Rf", 105: "Db", 106: "Sg", 107: "Bh", 108: "Hs", 109: "Mt", 110: "Ds", 111: "Rg", 112: "Cn", 113: "Nh", 114: "Fl", 115: "Mc", 116: "Lv", 117: "Ts", 118: "Og"
    }

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
                    if "Lp" in line:
                        continue

                    match = match.group(0).strip()
                    match_spl = match.split(" ")
                    match_spl[:] = [x.strip() for x in match_spl if x]
                    atom, coordx, coordy, coordz = match_spl

                    if atom.isnumeric():
                        atom = int(atom)
                        atom = convert_zvals_to_symbols(atom)
                        
                    coordx = f"{float(coordx) * bohr2aa:>10.10f}"
                    coordy = f"{float(coordy) * bohr2aa:>10.10f}"
                    coordz = f"{float(coordz) * bohr2aa:>10.10f}"
                    new_line = atom + " " + coordx + " " + coordy + " " + coordz 

                    f.write(new_line + "\n")

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
