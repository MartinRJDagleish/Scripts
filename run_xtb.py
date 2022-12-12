#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Author: Martin Dagleish (MRJD)

Version 0.5.9

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
# * 0.5.9  - Fixed file output depending on job type -> .xtbopt.xyz only in opt type jobs
# * 0.5.8  - Fixed wrong path string (previously only compat. with Windows) now works \ 
# *          on Linux and MacOS
# * 0.5.7  - Whitespace cleanup and made 'ext' same everywhere
# * 0.5.6  - Refactored code and move many subroutines to separate file.
# * 0.5.5  - Styling
# * 0.5.4  - Fixed "copy_file_list" not defined error -> default list is defined globally
# * 0.5.3  - Edge case with hess option fixed (correct files copied) and new_trj_filename added
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

VERSION = "0.5.9"

import os
import sys

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

import run_calc_mrjd as mrjd  # * My own module with subroutines

# from rich import inspect
# * ↑ for debugging

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
    help="The input file to change parameters for the calculation.\
          In the Turbomole (xcoord) format.",
)
xtb_parser.add_argument(
    "--add",
    nargs=argparse.REMAINDER,
    help="Any remaining arguments are passed to XTB.",
)
xtb_parser.add_argument("--version", action="version", version=f"{VERSION}")


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
            SOLVENT = mrjd.get_solvent(args.solvent)
            if SOLVENT:
                options.append("--alpb")
                options.append(SOLVENT)
            else:
                raise ValueError("Solvent not found")
        except ValueError:
            print(
                f"The solvent '{args.solvent}' is not supported.\n\
                  Possible solvents are:\n\n {', '.join(mrjd.solvent_dict.keys())}"
            )
            sys.exit(1)

    if args.uhf:
        multip = args.uhf
        options.append("--uhf")
        options.append(multip)

    # *---------------------------------#
    # * MAIN PROCEDURE STARTS HERE
    # *---------------------------------#

    temp1_path = mrjd.create_temp1_folder(cwd)
    # * copy .xyz file to temp1 folder
    mrjd.copy_file_temp(temp1_path, xyz_file)

    # * copy input file (if exists) to temp1 folder
    if args.input:
        mrjd.copy_file_temp(temp1_path, input_file)

    os.chdir(temp1_path)

    # *---------------------------------#
    # * Run the calculation
    # *---------------------------------#

    mrjd.xtb_call(xyz_file, job_type, options, namespace, addit_args)

    # *--------------------------------------------#
    # * Run rename of xtbopt.log for OPT jobs only
    # *--------------------------------------------#

    # * General output is in .out and depending on the job type, there are more files
    copy_file_list = [os.path.join(temp1_path, f"{namespace}.out")]

    if OPT_BOOL:
        renamed_file = mrjd.rename_file(namespace, "xtbopt.log", "xtbopt.trj.xyz")
        opt_geom_xyz_path = os.path.join(temp1_path, f"{namespace}.xtbopt.xyz")
        copy_file_list.append(os.path.join(temp1_path, renamed_file))
        copy_file_list.append(opt_geom_xyz_path)

    if HESS_BOOL:
        subprocess.run(
            [
                mrjd.obabel_bin,
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
            shell=mrjd.WIN_OS_BOOL,
        )

        if args.hess:
            copy_file_list = []
            copy_file_list.append(os.path.join(temp1_path, f"{namespace}.out"))
            # only in pure hess run needed
            copy_file_list.append(os.path.join(temp1_path, f"{namespace}_FREQ.molden"))

    if MD_BOOL:
        renamed_file = mrjd.rename_file(namespace, "xtb.trj", "xtb.trj.xyz")
        copy_file_list.append(os.path.join(temp1_path, renamed_file))

    os.chdir("..")

    mrjd.copy_important_files_to_cwd(copy_file_list, cwd)

    # * OLD CODE
    if args.chem3d:
        # * Additional conversion to "chem3d format"
        print(45 * "-")
        print("*" + "Converting to chem3d format (tinker.xyz)".center(43, " ") + "*")
        print(45 * "-")

        # * Run obabel
        subprocess.run(
            [
                mrjd.obabel_bin,
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
            shell=mrjd.WIN_OS_BOOL,
        )

        print(45 * "-")
        print("*" + "Additional conversion to chem3d format done".center(43, " ") + "*")
        print(45 * "-")
