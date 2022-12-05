#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Author: Martin Dagleish (MRJD)

Version 0.5.2

This script is a wrapper for the XTB programme. It is designed 
to be a modular and easy to use script for the user. 
The common calculation that is done a geometry optimization and a 
frequency calculation (kwarg: --ohess). The use can change it though and with the 
--add keyword additional keywords may be passed to the XTB programme.

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
# * 0.5.2  - Fixed copy_file_list typo for MD option 
# * 0.5.1  - Rewrote the whole script:
# *        - Added booleans for OS, OPT, HESS and MD to make the code more readable.
# *        - Added more ternay operators to make the code more readable and more compact.
# *        - Added version option 
# *        - Made the option more consistent. 
# *        - Added input file options with automatic file type detection. (same namespace)
# * 0.5.0  - Added MD functionality to the script. (--omd, --md and --input)
# * 0.4.14 - Cleanup of code and made it more consistent.
# * 0.4.13 - Added space in print to stdout
# * 0.4.12 - Minor typos and bug fixes.
# * 0.4.11 - Added additional kwargs to pass to xtb (activate with --add) and fixed --opt to work as intended
# * 0.4.10 - Added ESP option to script. (Visualization is not known yet -> potentially openbabel usage needed)
# * 0.4.9 - Added UHF option to script.
# * 0.4.8 - Added possibility to until run hess without opt and actual center string.
# * 0.4.7 - Added version info to script
# * 0.4.6 - Fixed Linux not working as stdout has to be written via python and not ">"
# * 0.4.5 - Added os.path.basename(xyz_file) to get the name of the xyz file and removing
# *         any autocomplete characters from the name.
# * 0.4.4 - try-except for installation of xtb and obabel if not found
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

VERSION = "0.5.2"

import os
import sys

# from rich import inspect
# * ↑ for debugging

try:
    import argparse
except ImportError:
    print("Please install argparse. E.g. 'pip install argparse'")
    sys.exit(1)
try:
    import subprocess
except ImportError:
    print("Please install subprocess. E.g. 'pip install subprocess'")
    sys.exit(1)

#!##############################################################################
#!                                 PART 1                                      #
#!##############################################################################
#! Check if programms are all installed in order for the script to work.

# * Show the OS running this script
OPERATING_SYTEM = sys.platform
WIN_OS_BOOL = (
    False if sys.platform in ("darwin", "linux", "linux2") else True
)  # * Check if OS is Windows

#! Part 1.1 -> Check if xtb and obabel are installed and then
#! find the correct path to the xtb executable and store in variable
# * Get the right xtb executable format depending on the OS
try:
    XTB_PATH = (
        subprocess.run(
            ["where.exe", "xtb"], stdout=subprocess.PIPE, check=True
        ).stdout.decode("utf-8")
        if WIN_OS_BOOL
        else subprocess.run(
            ["which", "xtb"], stdout=subprocess.PIPE, check=True
        ).stdout.decode("utf-8")
    )
    xtb_bin = XTB_PATH.strip()
except subprocess.CalledProcessError:
    print("xtb not found. Please install xtb and make sure it is added to PATH.")
    sys.exit(1)


#! Part 1.2 -> Search for OpenBabel (obabel) executable
try:
    OPENBABEL_PATH = (
        subprocess.run(
            ["where.exe", "obabel"], stdout=subprocess.PIPE, check=True
        ).stdout.decode("utf-8")
        if WIN_OS_BOOL
        else subprocess.run(
            ["which", "obabel"], stdout=subprocess.PIPE, check=True
        ).stdout.decode("utf-8")
    )
    obabel_bin = OPENBABEL_PATH.strip()
except subprocess.CalledProcessError:
    print(
        "obabel not found. Please install OpenBabel and make sure it is added to PATH, \
         if you want to use the full capability of this scipt."
    )
    sys.exit(1)


#!##############################################################################
#!                                 PART 2                                      #
#!##############################################################################
#! Create parser to get the arguments from the command line.

# * Create the parser
xtb_parser = argparse.ArgumentParser(
    prog="run_xtb.py",
    usage="%(prog)s xyz_file [options]",
    description=f"Run a XTB calculation for a given xyz file. \
        Optimization and frequency calculations are done per default. -> Script Version {VERSION}",
)
xtb_parser.add_argument(
    "xyz_file",  #! Positional argument
    metavar="xyz_file",
    type=str,
    help="The xyz file to run the calculation on. Add .xyz extension to name (e.g. my_mol.xyz)",
)
xtb_parser.add_argument(
    "--opt",
    action="store_true",
    help="If you only want to run the geometry optimization without frequency \
        analysis / thermochemistry.",
)
xtb_parser.add_argument(
    "--hess",
    "--freq",
    action="store_true",
    help="If you only want to run the frequency calculation without optimization.",
)
xtb_parser.add_argument(
    "-C",
    "--chrg",  #! Optional argument
    metavar="charge",
    type=int,
    default="0",
    help="The charge of the molecule. (default: %(default)s)",
)
xtb_parser.add_argument(
    "-P",
    "--parallel",  #! Optional argument
    metavar="ncores",
    type=int,
    default=4,
    help="Number of cores for parallel calculation. (default: %(default)s)",
)
xtb_parser.add_argument(
    "-N",
    "--namespace",  #! Optional argument
    metavar="Name",
    type=str,
    help="The name of the calculation",
)
xtb_parser.add_argument(
    "-v",  #! Optional argument
    "--verbose",
    action="store_true",
    default=False,
    help="Longer output. (default: %(default)s)",
)
xtb_parser.add_argument(
    "--lmo", action="store_true", help="Localization of orbitals."  #! Optional argument
)
xtb_parser.add_argument(
    "--molden",
    action="store_true",
    help="Molden output for orbitals.",  #! Optional argument
)
xtb_parser.add_argument(
    "-S",
    "--solvent",
    metavar="SOLVENT",
    type=str,
    help="The solvent to use for the calculation. Possible solvents \
          (or common short names): \
          acetonitrile, aniline, benzaldehyde, benzene, ch2cl2, chcl3, \
          cs2, dioxane, dmf, dmso, ether, ethylacetate, furane, hexandecane,\
          hexane, methanol, nitromethane, octanol, woctanol, phenol, toluene, \
          thf, h2o. (ALPB methode)",
)
xtb_parser.add_argument(
    "--uhf",
    type=str,
    metavar="MULT",
    help="If you want to run in unrestricted Hartree Fock mode to account for \
        non-Singulett states.",
)
xtb_parser.add_argument(
    "--chem3d",
    action="store_true",
    help="If you want to use the Chem3D to view the resulting xyz. (Tinker xyz)",
)
xtb_parser.add_argument(
    "--esp",
    action="store_true",
    help="Calculate the electrostatic potential on VdW-grid.",
)
xtb_parser.add_argument(
    "--omd",
    action="store_true",
    help="Run and MD calculation, but optimize the geometry first.",
)
xtb_parser.add_argument(
    "--md",
    action="store_true",
    help="Run and MD calculation wihout optimization first.",
)
xtb_parser.add_argument(
    "--input",
    metavar="INPUT",
    type=str,
    help="The input file to change parameters for the calculation. In the Turbomole (xcoord) format.",
)
xtb_parser.add_argument(
    "--add",
    nargs=argparse.REMAINDER,
    help="Any remaining arguments are passed to XTB.",
)
xtb_parser.add_argument("--version", action="version", version=f"{VERSION}")

solvent_dict = {
    "acetone": ["acetone", "Aceton", "(CH3)2CO"],
    "acetonitrile": ["acetonitrile", "ACN", "Acetonitrile", "Acetonitril", "AcN"],
    "aniline": ["aniline", "ANI", "Aniline", "Anil"],
    "benzaldehyde": ["benzaldehyde", "BEN", "Benzaldehyde", "Benzal", "Benzaldehyd"],
    "benzene": ["benzene", "Benzene", "Benzol"],
    "ch2cl2": ["ch2cl2", "CH2CL2", "DCM", "Dichloromethane", "Dichlormethan"],
    "chcl3": ["chcl3", "CHCL3", "Chloroform", "Chloroforme", "chloroform"],
    "ccl4": ["ccl4", "CCl4", "Carbontet", "Tetrachlormethan"],
    "cs2": ["cs2", "CS2", "Carbonsulfide", "Carbonsulfid", "carbonsulfide"],
    "dioxane": ["dioxane", "Dioxane", "Dioxal"],
    "dmf": ["dmf", "DMF", "Dimethylformamide", "Dimethylformamid", "dimethylformamide"],
    "dmso": ["dmso", "DMSO", "Me2SO"],
    "ether": ["ether", "ETHER", "Ether", "diethylether", "Diethylether"],
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


# * Execute the parse_args() method
args = xtb_parser.parse_args()
addit_args = args.add if args.add else []
# print(inspect(args)) #* for debugging

#! Run the calculation, acutal programm:
if __name__ == "__main__":
    cwd = os.getcwd()
    xyz_file = os.path.basename(args.xyz_file)

    # * Gather the options for the calculation
    options = []

    # * Define and check the name of the job (needed for input file)
    if args.namespace:  #! If the user has defined a namespace, use it
        namespace = args.namespace
        options.append("--namespace")
        options.append(namespace)
    else:  #! If not, use the name of the xyz file
        namespace = os.path.splitext(os.path.basename(xyz_file))[0]
        options.append("--namespace")
        options.append(namespace)  # * this has to be a new entry

    # * Check if the user added an input file manually
    if args.input:
        options.append("--input")
        # * Check if the input file exists and is a file
        if os.path.isfile(args.input):
            input_file = os.path.basename(args.input)
            options.append(input_file)
        else:
            print(f"The input file {args.input} does not exist.")
            sys.exit(1)

    # * The type of job: (O)MD, GeoOpt, SP, Hess,
    job_type = []

    OPT_BOOL, HESS_BOOL = True, True
    MD_BOOL = False

    if args.omd:
        job_type.append("--omd")
        HESS_BOOL, MD_BOOL = False, True
        if not args.input:
            if os.path.isfile(os.path.join(cwd, f"{namespace}.inp")):
                # * If no input file is given, search for .inp with namespace as xyz_file
                options.append("--input")
                options.append(f"{namespace}.inp")
                input_file = args.input = f"{namespace}.inp"
            else:
                print("You need to specify an input file for the MD calculation.")
                sys.exit(1)
    elif args.md:
        job_type.append("--md")
        OPT_BOOL, HESS_BOOL, MD_BOOL = False, False, True
        if not args.input:
            if os.path.isfile(os.path.join(cwd, f"{namespace}.inp")):
                # * If no input file is given, search for .inp with namespace as xyz_file
                options.append("--input")
                options.append(f"{namespace}.inp")
                input_file = args.input = f"{namespace}.inp"
            else:
                print("You need to specify an input file for the MD calculation.")
                sys.exit(1)
    else:
        if args.hess:
            job_type.append("--hess")
            OPT_BOOL = False
        elif args.opt:
            job_type.append("--opt")
            HESS_BOOL = False
        else:
            job_type.append("--ohess")
        # * Why would one do a SP with XTB? -> not implemented
        # * use xtb direct call instead …

    if args.chrg:
        options.append("--chrg")
        options.append(str(args.chrg))
    else:
        options.append("--chrg")
        options.append("0")

    # ? Add --parallel option ALWAYS, only the ncore changes
    options.append("--parallel")
    options.append(str(args.parallel))

    if args.verbose:
        options.append("--verbose")

    if args.lmo:
        options.append("--lmo")

    if args.molden:
        options.append("--molden")

    if args.esp:
        options.append("--esp")

    if args.solvent:
        try:
            SOLVENT = get_solvent(args.solvent)
            if SOLVENT:
                options.append("--alpb")
                options.append(SOLVENT)
            else:
                raise ValueError("Solvent not found")
        except ValueError:
            print(
                f"The solvent '{args.solvent}' is not supported.\nPossible solvents are:\n\n {', '.join(solvent_dict.keys())}"
            )
            sys.exit(1)

    if args.uhf:
        multip = args.uhf
        options.append("--uhf")
        options.append(multip)

    # * mkdir temp1 folder for xtb files
    temp1_path = os.path.join(cwd, "temp1")
    if not os.path.isdir(temp1_path):
        os.mkdir(temp1_path)

    # * copy .xyz file to temp1 folder
    _ = (
        os.system(f"copy {xyz_file} {temp1_path}")
        if WIN_OS_BOOL
        else os.system(f"cp {xyz_file} {temp1_path}")
    )

    # * copy input file (if exists) to temp1 folder
    if args.input:
        _ = (
            os.system(f"copy {input_file} {temp1_path}")
            if WIN_OS_BOOL
            else os.system(f"cp {input_file} {temp1_path}")
        )

    ############################
    # * change to temp1 folder
    ############################
    os.chdir(temp1_path)

    # *---------------------------------#
    # * Run the calculation
    # ? you should not use os.system -> use subprocess.run instead
    # *---------------------------------#

    xtb_call_cmds = [f"{xtb_bin}", f"{xyz_file}", *job_type, *options, *addit_args]
    # * if addit_args is empty it is ignored
    with open(f"{namespace}.out", "w", encoding="utf-8") as out:
        subprocess.run(
            xtb_call_cmds,
            stdout=out,
            check=True,
            shell=WIN_OS_BOOL,
            text=True,  # * to capture stdout as string
        )
    # *---------------------------------#

    print(36 * "-")
    print("*" + "XTB RUN FINISHED!".center(34, " ") + "*")
    print(36 * "-")

    # * End of job
    # * 1. Run obabel to convert the output to .molden format if HESS_BOOL is True
    # * 2. Move the '_FREQ.molden' file to the original folder

    # *--------------------------------------------#
    # * Run rename of xtbopt.log for OPT jobs only
    # *--------------------------------------------#
    if OPT_BOOL:
        if not os.path.isfile(f"{namespace}.xtbopt.trj.xyz"):
            os.rename(f"{namespace}.xtbopt.log", f"{namespace}.xtbopt.trj.xyz")
        else:
            os.remove(f"{namespace}.xtbopt.trj.xyz")
            os.rename(f"{namespace}.xtbopt.log", f"{namespace}.xtbopt.trj.xyz")

        copy_file_list = [
            f"{temp1_path}\\{namespace}{ext}"
            for ext in (
                ".out",
                ".xtbopt.trj.xyz",
                ".xtbopt.xyz",
            )
        ]

    if HESS_BOOL:
        subprocess.run(
            [
                obabel_bin,
                f"{namespace}.g98.out",
                "-i",
                "g98",
                "-o",
                "molden",
                "-O",
                f"{namespace}_FREQ.molden",
            ],
            stdout=subprocess.PIPE,
            check=True,
            shell=WIN_OS_BOOL,
        )

        if args.hess:
            copy_file_list = []

        copy_file_list.append(f"{temp1_path}\\{namespace}_FREQ.molden")

    if MD_BOOL:
        trj_filename = f"{namespace}.xtb.trj"
        # * rename the xtb.trj file to .xtb.trj.xyz
        os.rename(trj_filename, f"{namespace}.xtb.trj.xyz")
        # * add the .xtb.trj.xyz file to the copy list
        copy_file_list.append(f"{temp1_path}\\{namespace}.xtb.trj.xyz")

    os.chdir("..")

    copy_cmds = [
        ("copy " + filename + " " + cwd).split()
        if WIN_OS_BOOL
        else ("cp " + filename + " " + cwd).split()
        for filename in copy_file_list
    ]
    _ = [subprocess.run(cmd, check=True, shell=WIN_OS_BOOL) for cmd in copy_cmds]

    print(37 * "-")
    print("*" + "Importants files copied to CWD".center(35, " ") + "*")
    print(37 * "-")

    # * OLD CODE
    if args.chem3d:
        # * Additional conversion to "chem3d format"
        print(45 * "-")
        print("*" + "Converting to chem3d format (tinker.xyz)".center(43, " ") + "*")
        print(45 * "-")

        # * Run obabel
        subprocess.run(
            [
                obabel_bin,
                f"{namespace}.xtbopt.xyz",
                "-i",
                "xyz",
                "-o",
                "txyz",
                "-O",
                f"{namespace}_tinker.xyz",
            ],
            stdout=subprocess.PIPE,
            check=True,
            shell=WIN_OS_BOOL,
        )

        print(45 * "-")
        print("*" + "Conversion to chem3d format done".center(43, " ") + "*")
        print(45 * "-")
