#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Author: Martin Dagleish (MRJD)

Version 0.1.0

This script is used to run the ORCA program.

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
    import argparse
except ImportError:
    print("Please install argparse. Via pip install argparse")
    sys.exit()
try:
    import subprocess
except ImportError:
    print("Please install subprocess. Via pip install subprocess")
    sys.exit()

#!##############################################################################
#!                                 PART 1                                      #
#!##############################################################################


# * Show the OS running this script
OPERATING_SYTEM = sys.platform

#! Part 1.1 -> xtb installation and path finding

#* This is a HIGHLY custom directory for the ORCA programme, but the problem is
#* that Linux already has a 'ORCA' programme (screen reader) which means that 
#* the path has to be added manually. (Or at least I don't know how to do it)
if OPERATING_SYTEM in ("linux", "linux2"):
    ORCA_PATH = "/loctmp/dam63759/orca/orca"
elif OPERATING_SYTEM == "win32":
    ORCA_PATH = r"C:\ORCA\orca.exe"

# #! Part 1.2 -> Search for OpenBabel (obabel) executable
# if OPERATING_SYTEM in ("linux", "linux2", "darwin"):
#     OPENBABEL_PATH = subprocess.run(
#         ["which", "obabel"], stdout=subprocess.PIPE, check=True
#     ).stdout.decode("utf-8")
#     obabel = OPENBABEL_PATH.strip()
# elif OPERATING_SYTEM == "win32":
#     OPENBABEL_PATH = subprocess.run(
#         ["where.exe", "obabel"], stdout=subprocess.PIPE, check=True
#     ).stdout.decode("utf-8")
#     obabel = OPENBABEL_PATH.strip()
# else:
#     print("Is OpenBabel installed on this OS?")
#     print("Make sure OpenBabel is added to path.")
#     sys.exit()


#!##############################################################################
#!                                 PART 2                                      #
#!##############################################################################
#! Create parser to get the arguments from the command line.

# * Create the parser
orca_parser = argparse.ArgumentParser(
    prog="run_orca.py",
    usage="%(prog)s input-file [options]",
    description="Run an ORCA calculation for a given input file.",
)

orca_parser.add_argument(
    "input_file",  #! Positional argument
    metavar="INPUT-FILE",
    type=str,
    help="The input-file to run the calculation on. Either with or without extension.",
)

#! Possible future options:
# orca_parser.add_argument(
#     "--ir-spec-plot",
#     "-ir-plot",
#     action="store_true",
#     help="Plot the IR spectrum."
# )


# solvent_dict = {
#     "acetonitrile": ["acetonitrile", "ACN", "Acetonitrile", "Acetonitril", "AcN"],
#     "aniline": ["aniline", "ANI", "Aniline", "Anil"],
#     "benzaldehyde": ["benzaldehyde", "BEN", "Benzaldehyde", "Benzal", "Benzaldehyd"],
#     "benzene": ["benzene", "Benzene", "Benzol"],
#     "ch2cl2": ["ch2cl2", "CH2CL2", "DCM", "Dichloromethane", "Dichlormethan"],
#     "chcl3": ["chcl3", "CHCL3", "Chloroform", "Chloroforme", "chloroform"],
#     "cs2": ["cs2", "CS2", "Carbonsulfide", "Carbonsulfid", "carbonsulfide"],
#     "dioxane": ["dioxane", "Dioxane", "Dioxal"],
#     "dmf": ["dmf", "DMF", "Dimethylformamide", "Dimethylformamid", "dimethylformamide"],
#     "dmso": ["dmso", "DMSO", "Me2SO"],
#     "ether": ["ether", "ETHER", "Ether"],
#     "ethylacetate": ["ethylacetate", "ETAC", "Ethylacetat", "Ethylacetate"],
#     "furane": ["furane", "FUR", "Furan"],
#     "hexandecane": ["hexandecane", "HEX", "Hexandecane"],
#     "hexane": ["hexane", "HEX", "Hexane", "Hexan"],
#     "methanol": ["methanol", "METH", "Methanol"],
#     "nitromethane": ["nitromethane", "NIT", "Nitromethane", "Nitromethan"],
#     "octanol": ["octanol", "OCT", "Oct-OH"],
#     "woctanol": ["woctanol", "WOCT", "Water octanol", "Wasser_Octanol"],
#     "phenol": ["phenol", "PHEN", "Phenol"],
#     "toluene": ["toluene", "TOL", "Toluene", "Toluol"],
#     "thf": ["thf", "THF", "Tetrahydrofuran", "tetrahydrofurane"],
#     "water": ["water", "WAT", "Water", "Wasser", "H2O", "h2o"],
# }

# * Execute the parse_args() method
args = orca_parser.parse_args()

#! Run the calculation, acutal programm:
if __name__ == "__main__":
    cwd = os.getcwd()

    input_file = args.input_file
    if input_file.endswith(".inp"):
        pass
    else:
        input_file += ".inp"

    namespace = os.path.splitext(input_file)[0]

    # * mkdir temp1 folder for xtb files
    temp1_path = os.path.join(cwd, "temp1")
    if not os.path.isdir(temp1_path):
        os.mkdir(temp1_path)

    # * copy .xyz file to temp1 folder
    if OPERATING_SYTEM == "win32":
        os.system(f"copy {input_file} {temp1_path}")
    else:
        os.system(f"cp {input_file} {temp1_path}")

    os.chdir(temp1_path)

    # *---------------------------------#
    # * Run the calculation
    if OPERATING_SYTEM in ("win32", "Windows"):
        subprocess.run([f"{ORCA_PATH}", input_file, ">", f"{namespace}.out"],
             stdout=subprocess.PIPE, shell=True, check=True)
    elif OPERATING_SYTEM in ("linux", "Linux", "Darwin"):
        subprocess.run([f"{ORCA_PATH}", input_file, ">", f"{namespace}.out"],
             stdout=subprocess.PIPE, check=True)
    # *---------------------------------#

    print("---------------------------------")
    print("*      ORCA RUN SUCCESSFUL!      *")
    print("---------------------------------")

    os.chdir("..")
    if OPERATING_SYTEM in ("win32", "Windows"):
        subprocess.run(["copy", f"{temp1_path}\\{namespace}.out", cwd],
             stdout=subprocess.PIPE, shell=True, check=True)
    elif OPERATING_SYTEM in ("linux", "Linux", "Darwin"):
        subprocess.run(["cp", f"{temp1_path}\\{namespace}.out", cwd],
             stdout=subprocess.PIPE, check=True)

    print("------------------------------------")
    print("*       Output copied to CWD       *")
    print("------------------------------------")