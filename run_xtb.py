#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Author: Martin Dagleish (MRJD)

Version 0.4.3

This script is used to run the XTB program and convert the
output .g98 to .molden format
in order to process the output in ChemCraft.

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
# * 0.4.3 - Added Chem3D cmd and fixed Linux imcompatibility
# * 0.4.2 - Added support for Linux and MacOS
# * 0.4.1 - Added support for multiple solvent types and raise error if user input is not valid
# * 0.4.0 - Added conversion from .g98 to .molden format and added .trj.xyz output
# *         This allows for easier reading of the .trj.xyz file and for visualization
# *         in ChemCraft.
# * 0.3.2 - Fixed bug where XTB would not run if the input file was not found.
# * 0.3.1 - Added try and except for imports and added a check for the xtb executable
# * 0.3.0 - Added support for multiple operating systems to
# *       find the correct xtb executable
# * 0.2.0 - Rewrote the options to be one option for xtb-call.
# *       This is easier to use and more flexible.
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
#! Check if programms are all installed in order for the script to work.

# * Show the OS running this script
OPERATING_SYTEM = sys.platform


#! Part 1.1 -> xtb installation and path finding

# * Get the right xtb executable format depending on the OS
if OPERATING_SYTEM in ("linux", "linux2", "darwin"):
    XTB_PATH = subprocess.run(
        ["which", "xtb"], stdout=subprocess.PIPE, check=True
    ).stdout.decode("utf-8")
    xtb = XTB_PATH.strip()
elif OPERATING_SYTEM == "win32":
    # xtb = "xtb.exe"
    XTB_PATH = subprocess.run(
        ["where.exe", "xtb"], stdout=subprocess.PIPE, check=True
    ).stdout.decode("utf-8")
    xtb = XTB_PATH.strip()
else:
    print("Is XTB installed on this OS?")
    print("Make sure XTB is added to path.")
    sys.exit()

#! Part 1.2 -> Search for OpenBabel (obabel) executable
if OPERATING_SYTEM in ("linux", "linux2", "darwin"):
    OPENBABEL_PATH = subprocess.run(
        ["which", "obabel"], stdout=subprocess.PIPE, check=True
    ).stdout.decode("utf-8")
    obabel = OPENBABEL_PATH.strip()
elif OPERATING_SYTEM == "win32":
    OPENBABEL_PATH = subprocess.run(
        ["where.exe", "obabel"], stdout=subprocess.PIPE, check=True
    ).stdout.decode("utf-8")
    obabel = OPENBABEL_PATH.strip()
else:
    print("Is OpenBabel installed on this OS?")
    print("Make sure OpenBabel is added to path.")
    sys.exit()


#!##############################################################################
#!                                 PART 2                                      #
#!##############################################################################
#! Create parser to get the arguments from the command line.

# * Create the parser
xtb_parser = argparse.ArgumentParser(
    prog="run_xtb.py",
    usage="%(prog)s xyz_file [options]",
    description="Run a XTB calculation for a given xyz file. \
        Optimization and frequency calculations are done per default.",
)

xtb_parser.add_argument(
    "xyz_file",  #! Positional argument
    metavar="xyz_file",
    type=str,
    help="The xyz file to run the calculation on. Add .xyz extension to name (e.g. my_mol.xyz)",
)
# xtb_parser.add_argument('--ohess',              #! Optional argument
#                         action="store_true",
#                         help='Optimize the geometry and calculate the Hessian')
xtb_parser.add_argument(
    "-c",
    "--chrg",  #! Optional argument
    metavar="charge",
    type=int,
    default="0",
    help="The charge of the molecule",
)
xtb_parser.add_argument(
    "-P",
    "--parallel",  #! Optional argument
    metavar="ncores",
    type=int,
    default=1,
    help="Number of cores for parallel calculation",
)
xtb_parser.add_argument(
    "-n",
    "--namespace",  #! Optional argument
    metavar="Name",
    type=str,
    help="The name of the calculation",
)
xtb_parser.add_argument(
    "-v",  #! Optional argument
    "--verbose",
    action="store_true",
    help="Longer output. Default is False",
)
xtb_parser.add_argument(
    "-lmo", action="store_true", help="Localization of orbitals."  #! Optional argument
)
xtb_parser.add_argument(
    "-molden",
    action="store_true",
    help="Molden output for orbitals.",  #! Optional argument
)
xtb_parser.add_argument(
    "-s",
    "--solvent",
    metavar="SOLVENT",
    type=str,
    help="The solvent to use for the calculation. Possible solvents \
          (or common short names): \
          acetonitrile, aniline, benzaldehyde, benzene, ch2cl2, chcl3, \
          cs2, dioxane, dmf, dmso, ether, ethylacetate, furane, hexandecane,\
          hexane, methanol, nitromethane, octanol, woctanol, phenol, toluene, \
          thf, water. (ALPB methode)",
)
xtb_parser.add_argument(
    "--chem3d",
    action="store_true",
    help="If you want to use the Chem3D to view the resulting xyz.",
)
#! Possible future options:
# xtb_parser.add_argument(
#     "--ir-spec-plot",
#     "-ir-plot",
#     action="store_true",
#     help="Plot the IR spectrum."
# )


solvent_dict = {
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
    "ether": ["ether", "ETHER", "Ether"],
    "ethylacetate": ["ethylacetate", "ETAC", "Ethylacetat", "Ethylacetate"],
    "furane": ["furane", "FUR", "Furan"],
    "hexandecane": ["hexandecane", "HEX", "Hexandecane"],
    "hexane": ["hexane", "HEX", "Hexane", "Hexan"],
    "methanol": ["methanol", "METH", "Methanol"],
    "nitromethane": ["nitromethane", "NIT", "Nitromethane", "Nitromethan"],
    "octanol": ["octanol", "OCT", "Oct-OH"],
    "woctanol": ["woctanol", "WOCT", "Water octanol", "Wasser_Octanol"],
    "phenol": ["phenol", "PHEN", "Phenol"],
    "toluene": ["toluene", "TOL", "Toluene", "Toluol"],
    "thf": ["thf", "THF", "Tetrahydrofuran", "tetrahydrofurane"],
    "water": ["water", "WAT", "Water", "Wasser", "H2O", "h2o"],
}

def get_solvent(solvent_user_inp):
    """
    Helper function for solvent from solvent_dict.
    """
    for solvent, solvent_names in solvent_dict.items():
        if solvent_user_inp in solvent_names:
            return solvent


# * Execute the parse_args() method
args = xtb_parser.parse_args()

#! Run the calculation, acutal programm:
if __name__ == "__main__":
    cwd = os.getcwd()
    xyz_file = args.xyz_file

    # * Gather the options for the calculation
    options = []
    if args.chrg:
        options.append("--chrg")
        options.append(str(args.chrg))
    else:
        options.append("--chrg")
        options.append("0")

    if args.parallel > 1:
        options.append("--parallel")
        options.append(str(args.parallel))

    if args.namespace:
        namespace = args.namespace
        options.append("--namespace")
        options.append(args.namespace)
    else:
        namespace = os.path.splitext(os.path.basename(xyz_file))[0]
        options.append("--namespace")
        options.append(namespace)
        options.append(f" > {namespace}.out")

    if args.verbose:
        options.append("--verbose")

    if args.lmo:
        options.append("--lmo")

    if args.molden:
        options.append("--molden")

    if args.solvent:
        try:
            SOLVENT = get_solvent(args.solvent)
            if SOLVENT:
                options.append(f"--alpb {SOLVENT}")
            else:
                raise ValueError("Solvent not found")
        except ValueError:
            print(
                f"The solvent '{args.solvent}' is not supported.\nPossible solvents are:\n\n {', '.join(solvent_dict.keys())}"
            )
            sys.exit()

    # * mkdir temp1 folder for xtb files
    temp1_path = os.path.join(cwd, "temp1")
    if not os.path.isdir(temp1_path):
        os.mkdir(temp1_path)

    # * copy .xyz file to temp1 folder
    if OPERATING_SYTEM == "win32":
        os.system(f"copy {xyz_file} {temp1_path}")
    else:
        os.system(f"cp {xyz_file} {temp1_path}")

    os.chdir(temp1_path)

    # *---------------------------------#
    # * Run the calculation
    os.system(f"{xtb} {xyz_file} --ohess {' '.join(options)}")
    # *---------------------------------#

    print("---------------------------------")
    print("*      XTB RUN SUCCESSFUL!      *")
    print("---------------------------------")

    # * End of job
    # * 1. Run obabel to convert the output to .molden format
    # * 2. Move the '_FREQ.molden' file to the original folder

    # * Run obabel
    if OPERATING_SYTEM in ("win32","Windows"):
        subprocess.run(
            [
                obabel,
                f"{namespace}.g98.out",
                "-i",
                "g98",
                "-o",
                "molden",
                "-O",
                f"{namespace}_FREQ.molden",
            ],
            stdout=subprocess.PIPE,
            shell=True,
            check=True,
        )
    else:
        subprocess.run(
            [
                obabel,
                f"{namespace}.g98.out",
                "-i",
                "g98",
                "-o",
                "molden",
                "-O",
                f"{namespace}_FREQ.molden",
            ],
            stdout=subprocess.PIPE,
            check=True
        )

    if not os.path.isfile(f"{namespace}.xtbopt.trj.xyz"):
        os.rename(f"{namespace}.xtbopt.log", f"{namespace}.xtbopt.trj.xyz")
    else:
        os.remove(f"{namespace}.xtbopt.trj.xyz")
        os.rename(f"{namespace}.xtbopt.log", f"{namespace}.xtbopt.trj.xyz")

    os.chdir("..")
    if OPERATING_SYTEM in ("win32", "Windows"):
        copy_cmds = [
            ("copy " + f"{temp1_path}\\{namespace}{ext} " + cwd).split()
            for ext in (
                ".out",
                "_FREQ.molden",
                ".xtbopt.trj.xyz",
                ".xtbopt.xyz",
            )  #! Copy the output files to the original folder
        ]
        for cmd in copy_cmds:
            subprocess.run(cmd, stdout=subprocess.PIPE, shell=True, check=True)
    elif OPERATING_SYTEM in ("linux", "Linux", "Darwin"):
        copy_cmds = [
            ("cp " + f"{temp1_path}/{namespace}{ext} " + cwd).split()
            for ext in (
                ".out",
                "_FREQ.molden",
                ".xtbopt.trj.xyz",
                ".xtbopt.xyz",
            )  #! Copy the output files to the original folder
        ]
        for cmd in copy_cmds:
            subprocess.run(cmd, stdout=subprocess.PIPE, check=True)

    print("------------------------------------")
    print("*  Importants files copied to CWD  *")
    print("------------------------------------")

    if args.chem3d:
        print("----------------------------------------------")
        print("*  Converting to chem3d format (tinker.xyz)  *")
        print("----------------------------------------------")

        # * Run obabel
        if OPERATING_SYTEM in ("win32","Windows"):
            subprocess.run(
                [
                    obabel,
                    f"{namespace}.xtbopt.xyz",
                    "-i",
                    "xyz",
                    "-o",
                    "txyz",
                    "-O",
                    f"{namespace}_tinker.xyz",
                ],
                stdout=subprocess.PIPE,
                shell=True,
                check=True,
            )
        else:
            subprocess.run(
                [
                    obabel,
                    f"{namespace}.xtbopt.xyz",
                    "-i",
                    "xyz",
                    "-o",
                    "txyz",
                    "-O",
                    f"{namespace}_tinker.xyz",
                ],
                stdout=subprocess.PIPE,
                check=True
            )
        print("------------------------------------")
        print("*  Conversion to chem3d format done  *")
        print("------------------------------------")
