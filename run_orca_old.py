#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Author: Martin Dagleish (MRJD)

Version 0.3.2

This is a wrapper script for the ORCA programme.

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
# * 0.3.2 - Fixed bug with .hess file not being copied from frequency calculations
# * 0.3.1 - Added check for .hess file from frequency calculations
# * 0.3.0 - Simplified code and reduced checks needed for OS (Windows or Linux)
# * 0.2.5 - Added more output to cwd (.out, .hess and .xyz files)
# * 0.2.4 - Switched os.system for subprocess.run in script and updated Windows
# * 0.2.3 - Added option to copy multiple xyz files to temp1 if wanted.
# * 0.2.2 - Prettified printing of ORCA output.
# * 0.2.1 - Path slashes wrong for Linux
# * 0.2.0 - Fixed Linux not working as stdout has to be written via python and not ">"
# * 0.1.0 - Initial release

VERSION = "0.3.2"

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

# * Show the OS running this script
OPERATING_SYTEM = sys.platform
WIN_OS_BOOL = (
    False if sys.platform in ("darwin", "linux", "linux2") else True
)  # * Check if OS is Windows

#! NOTE:
# * This is a HIGHLY custom directory for the ORCA programme, but the problem is
# * that Linux already has a 'ORCA' programme (screen reader) which means that
# * the path has to be added manually. (Or at least I don't know how else to do it)
if WIN_OS_BOOL:
    ORCA_PATH = r"C:\ORCA\orca.exe"
else:
    ORCA_PATH = "/loctmp/dam63759/orca/orca"

# * Create the parser
orca_parser = argparse.ArgumentParser(
    prog="run_orca.py",
    usage="%(prog)s input-file [options]",
    description=f"Run an ORCA calculation for a given input file. -> Script Version {VERSION}",
)

orca_parser.add_argument(
    "input_file",  #! Positional argument
    metavar="INPUT-FILE",
    type=str,
    help="The input-file to run the calculation on. Either with or without extension.",
)

orca_parser.add_argument(
    "--xyz",  #! Positional argument
    metavar="XYZ-FILE",
    type=str,
    nargs="*",  # * = 0 or more arguments
    help="The xyz-file(s) to copy in temp1 (temporary folder for calculations). \
        Give a space separated list of xyz-files. E.g. --xyz xyz1.xyz xyz2.xyz",
)

#! Possible future options:
# orca_parser.add_argument(
#     "--ir-spec-plot",
#     "-ir-plot",
#     action="store_true",
#     help="Plot the IR spectrum."
# )


# * Execute the parse_args() method
args = orca_parser.parse_args()

#! Run the calculation, acutal programm:
if __name__ == "__main__":
    cwd = os.getcwd()

    input_file = (
        args.input_file
        if args.input_file.endswith(".inp")
        else args.input_file + ".inp"
    )
    namespace = os.path.splitext(input_file)[0]

    # * Check the type of job for copying .hess file:
    HESS_FILE = False
    with open(input_file, "r", encoding="utf-8") as f:
        for l_no, line in enumerate(f):
            if "freq" in line.lower():
                HESS_FILE = True
                break

    # * mkdir temp1 folder for xtb files
    temp1_path = os.path.join(cwd, "temp1")
    if not os.path.isdir(temp1_path):
        os.mkdir(temp1_path)

    # * copy .xyz file to temp1 folder
    if WIN_OS_BOOL:
        copy_cmd = "copy"
    else:
        copy_cmd = "cp"

    subprocess.run([copy_cmd, input_file, temp1_path], check=True, shell=WIN_OS_BOOL)

    if args.xyz:
        xyz_files = [xyz if xyz.endswith(".xyz") else xyz + ".xyz" for xyz in args.xyz]
        for xyz_file in xyz_files:
            if os.path.isfile(os.path.join(cwd, xyz_file)):
                subprocess.run(
                    [copy_cmd, xyz_file, temp1_path], check=True, shell=WIN_OS_BOOL
                )
            else:
                print(f"{xyz_file} not found in {cwd}")
                sys.exit(1)

    os.chdir(temp1_path)

    # *---------------------------------#
    # * Run the calculation
    with open(f"{namespace}.out", "w", encoding="utf-8") as out:
        subprocess.run(
            [f"{ORCA_PATH}", input_file],
            stdout=out,
            check=True,
            shell=WIN_OS_BOOL,
            text=True,
        )
    # *---------------------------------#

    print("\n" + 40 * "-")
    print("*" + "ORCA RUN FINISHED!".center(38, " ") + "*")
    print(40 * "-")

    os.chdir("..")

    extensions = ["out", "xyz"]
    if HESS_FILE:
        extensions.append("hess")

    copy_cmds = [
        (f"{copy_cmd} " + f"{temp1_path}/{namespace}.{ext} " + cwd).split()
        for ext in extensions
    ]

    for cmd in copy_cmds:
        subprocess.run(cmd, shell=WIN_OS_BOOL, check=True)

    print(40 * "-")
    print("*" + "Output copied to CWD".center(38, " ") + "*")
    print(40 * "-")
    sys.exit(0)
