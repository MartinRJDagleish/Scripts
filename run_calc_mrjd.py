#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Author: Martin Dagleish

Version 0.1.0

This is a refactoring of the run_orca.py and run_xtb.ply scripts
to make it easier to run calculations with different programs.

MIT License

Copyright (c) 2022 Martin Dagleish

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the 'Software'), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

# * Changelog
# * V 0.1.0  - Initial version

import os
import sys

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
OPERATING_SYTEM: str = sys.platform
WIN_OS_BOOL: bool = (
    False if sys.platform in ("darwin", "linux", "linux2") else True
)  # * Check if OS is Windows

#! Part 1.1 -> Check if xtb and obabel are installed and then
#! find the correct path to the xtb executable and store in variable
# * Get the right xtb executable format depending on the OS
try:
    XTB_PATH: str = (
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


def get_solvent(solvent_user_inp) -> str:
    """
    Helper function for solvent from solvent_dict.
    """
    for solvent, solvent_names in solvent_dict.items():
        if solvent_user_inp in solvent_names:
            return solvent


def create_temp1_folder(cwd: str) -> str:
    """
    Create a temporary folder for the calculations.
    """
    # * mkdir temp1 folder for xtb files
    temp1_path = os.path.join(cwd, "temp1")
    if not os.path.isdir(temp1_path):
        os.mkdir(temp1_path)
    return temp1_path


def copy_file_temp(temp1_path: str, filename: str) -> None:
    """
    Copy given file to temp1 folder.
    """
    _ = (
        os.system(f"copy {filename} {temp1_path}")
        if WIN_OS_BOOL
        else os.system(f"cp {filename} {temp1_path}")
    )


def xtb_call(
    xyz_file: str,
    job_type: list[str],
    options: list[str],
    namespace: str,
    addit_args: list[str],
) -> None:
    """
    Call xtb with the given arguments.
    """
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

def rename_file(namespace: str, old_ext: str, new_ext: str) -> str:
    """
    Rename file with given namespace and extensions.
    """
    if not os.path.isfile(f"{namespace}.{new_ext}"):
        os.rename(f"{namespace}.{old_ext}", f"{namespace}.{new_ext}")
    else:
        os.remove(f"{namespace}.{new_ext}")
        os.rename(f"{namespace}.{old_ext}", f"{namespace}.{new_ext}")
    return f"{namespace}.{new_ext}"

def copy_important_files_to_cwd(copy_file_list: list[str], cwd: str) -> None:
    """
    Copy important files to cwd.
    """
    for filename in copy_file_list:
        copy_cmd = ("copy " + filename + " " + cwd).split() \
        if WIN_OS_BOOL \
        else ("cp " + filename + " " + cwd).split()
        subprocess.run(copy_cmd, check=True, shell=mrjd.WIN_OS_BOOL) 
    print(37 * "-")
    print("*" + "Importants files copied to CWD".center(35, " ") + "*")
    print(37 * "-")
