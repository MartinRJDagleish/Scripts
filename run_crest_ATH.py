#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Author: Martin Dagleish (MRJD)

Version 0.1.0

This is a wrapper script for the CREST programme modifided for ATHENE 
on the HPC cluster at the University of Regensburg. 

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

# * Changelog
# * 0.1.0 - Initial release

VERSION = "0.1.0"

import os
import sys

try:
    import argparse
except ImportError:
    print("Please install argparse. Via pip install argparse")
    sys.exit(1)
try:
    import subprocess
except ImportError:
    print("Please install subprocess. Via pip install subprocess")
    sys.exit(1)


# * OS running this script
OPERATING_SYTEM = sys.platform

# * Create the parser
crest_parser = argparse.ArgumentParser(
    prog="run_crest.py",
    usage="%(prog)s input-file [options]",
    description=f"Run an CREST calculation for a given input file. -> Script Version {VERSION}",
)

crest_parser.add_argument(
    "xyz_file",  #! Positional argument
    metavar="XYZ-FILE",
    type=str,
    help="The xyz-file to run the calculation on.",
)
crest_parser.add_argument(
    "-s",
    "--solvent",  #! Positional argument
    metavar="SOLVENT",
    type=str,
    help="The solvent to use in the calculation (default: ALPB).",
)
crest_parser.add_argument(
    "-T",
    "--threads",  #! Optional argument
    metavar="ncores",
    type=int,
    default=4,
    help="Number of cores for parallel calculation. (default: %(default)s)",
)

# * Execute the parse_args() method
args = crest_parser.parse_args()


solvent_dict = {
    "acetone": ["acetone", "Aceton", "(CH3)2CO"],
    "acetonitrile": ["acetonitrile", "ACN", "Acetonitrile", "Acetonitril", "AcN"],
    "aniline": ["aniline", "ANI", "Aniline", "Anil"],
    "benzaldehyde": ["benzaldehyde", "BEN", "Benzaldehyde", "Benzal", "Benzaldehyd"],
    "benzene": ["benzene", "Benzene", "Benzol"],
    "ch2cl2": ["ch2cl2", "CH2CL2", "DCM", "Dichloromethane", "Dichlormethan"],
    "chcl3": ["chcl3", "CHCL3", "Chloroform", "Chloroforme", "chloroform"],
    "cs2": ["cs2", "CS2", "Carbonsulfide", "Carbonsulfid", "carbonsulfide"],
    "dioxane": ["dioxane", "Dioxane", "Dioxal"],
    "dmf": ["dmf", "DMF", "Dimethylformamide", "Dimethylformamid", "dimethylformamide"],
    "dmso": ["dmso", "DMSO", "Me2SO"],
    "ether": [
        "ether",
        "ETHER",
        "Ether",
        "diethylether",
        "Diethylether",
    ],  # * different names for xtb and for CREST
    "ethylacetate": ["ethylacetate", "ETAC", "Ethylacetat", "Ethylacetate"],
    "furane": ["furane", "FUR", "Furan"],
    "h2o": [
        "water",
        "WAT",
        "Water",
        "Wasser",
        "H2O",
        "h2o",
    ],  #! This was wrong -> "h2o" not "water"
    "hexandecane": ["hexandecane", "HEX", "Hexandecane"],
    "hexane": ["hexane", "HEX", "Hexane", "Hexan"],
    "methanol": ["methanol", "METH", "Methanol"],
    "nitromethane": ["nitromethane", "NIT", "Nitromethane", "Nitromethan"],
    "octanol": ["octanol", "OCT", "Oct-OH"],
    "woctanol": ["woctanol", "WOCT", "Water octanol", "Wasser_Octanol"],
    "phenol": ["phenol", "PHEN", "Phenol"],
    "toluene": ["toluene", "TOL", "Toluene", "Toluol"],
    "thf": ["thf", "THF", "Tetrahydrofuran", "tetrahydrofurane"],
}


def get_solvent(solvent_user_inp):
    """
    Helper function for solvent from solvent_dict.
    """
    for solvent, solvent_names in solvent_dict.items():
        if solvent_user_inp in solvent_names:
            return solvent


#! Run the calculation, acutal programm:
if __name__ == "__main__":
    cwd = os.getcwd()

    xyz_file = args.xyz_file
    filename, ext = os.path.splitext(xyz_file)
    namespace = filename.split(".")[0]  # * remove the .xtbopt or .xtb from the name

    # * Options for CREST run
    options = []
    options.append("--gfn2")  # * Use GFN2-xTB standard
    options.append("--nmr")  # * Use GFN2-xTB standard

    if args.solvent:
        try:
            SOLVENT = get_solvent(args.solvent)
            if SOLVENT:
                options.append(f"--alpb {SOLVENT}")
            else:
                raise ValueError("Solvent not found")
        except ValueError:
            print(
                f"The solvent '{args.solvent}' is not supported.\nPossible solvents are:\n\n \
                    {', '.join(solvent_dict.keys())}"
            )
            sys.exit(1)

    if args.threads >= 1:
        options.append("-T " + str(args.threads))

    # * mkdir tmp folder for CREST run
    crest_path = os.path.join(cwd, "crest_tmp")
    if not os.path.isdir(crest_path):
        os.mkdir(crest_path)

    # * copy .xyz file to tmp folder
    subprocess.run(["cp", xyz_file, crest_path], stdout=subprocess.PIPE, check=True)
    os.chdir(crest_path)

    # *---------------------------------#
    # * Run the calculation
    with open(f"{namespace}.out", "w", encoding="utf-8") as out:
        subprocess.run(["crest", f"{namespace}.xyz", *options], stdout=out, check=True)
    # *---------------------------------#

    print("\n" + 40 * "-")
    print("*" + "CREST RUN FINISHED!".center(38, " ") + "*")
    print(40 * "-")

    # os.chdir("..")
    copy_filelst = [
        "crest_conformers.xyz",
        "coord",
        "anmr_nucinfo",
        "anmr_rotamer",
    ]
    
    for filename in copy_filelst:
        if os.path.isfile(os.path.join(crest_path,filename)):
            subprocess.run(["cp", filename, cwd], stdout=subprocess.PIPE, check=True)
        else: 
            print(f"File {filename} not found! This may cause errors for CENSO!")        
            
    print("\n" + 40 * "-")
    print("*" + "COPYING DONE!".center(38, " ") + "*")
    print("*" + "YOU MAY START THE CENSO RUN NOW!".center(38, " ") + "*")
    print(40 * "-")
       
