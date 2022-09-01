#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Author: Martin Dagleish (MRJD)

Version 0.2.4

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
# * 0.2.4 - Switched os.system for subprocess.run in script and updated Windows 
# * 0.2.3 - Added option to copy multiple xyz files to temp1 if wanted.
# * 0.2.2 - Prettified printing of ORCA output.
# * 0.2.1 - Path slashes wrong for Linux
# * 0.2.0 - Fixed Linux not working as stdout has to be written via python and not ">"
# * 0.1.0 - Initial release

VERSION = "0.2.4"

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

#!##############################################################################
#!                                 PART 1                                      #
#!##############################################################################


# * Show the OS running this script
OPERATING_SYTEM = sys.platform

#! Part 1.1 -> xtb installation and path finding

# * This is a HIGHLY custom directory for the ORCA programme, but the problem is
# * that Linux already has a 'ORCA' programme (screen reader) which means that
# * the path has to be added manually. (Or at least I don't know how to do it)
if OPERATING_SYTEM in ("linux", "linux2"):
    ORCA_PATH = "/loctmp/dam63759/orca/orca"
elif OPERATING_SYTEM == "win32":
    ORCA_PATH = r"C:\ORCA\orca.exe"


#!##############################################################################
#!                                 PART 2                                      #
#!##############################################################################
#! Create parser to get the arguments from the command line.

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

    input_file = args.input_file
    if not input_file.endswith(".inp"):
        input_file += ".inp"

    namespace = os.path.splitext(input_file)[0]

    # * mkdir temp1 folder for xtb files
    temp1_path = os.path.join(cwd, "temp1")
    if not os.path.isdir(temp1_path):
        os.mkdir(temp1_path)

    # * copy .xyz file to temp1 folder
    if OPERATING_SYTEM == "win32":
        subprocess.run(
            ["copy", input_file, temp1_path], stdout=subprocess.PIPE, check=True, shell=True
        )
        if args.xyz:
            xyz_files = [
                xyz if xyz.endswith(".xyz") else xyz + ".xyz" for xyz in args.xyz
            ]
            for xyz_file in xyz_files:
                if os.path.isfile(os.path.join(cwd, xyz_file)):
                    subprocess.run(
                        ["copy", xyz_file, temp1_path],
                        stdout=subprocess.PIPE,
                        check=True,
                        shell=True
                    )
                else:
                    print(f"{xyz_file} not found in {cwd}")
                    sys.exit(1)
    else:
        subprocess.run(
            ["cp", input_file, temp1_path], stdout=subprocess.PIPE, check=True
        )
        if args.xyz:
            xyz_files = [
                xyz if xyz.endswith(".xyz") else xyz + ".xyz" for xyz in args.xyz
            ]
            for xyz_file in xyz_files:
                if os.path.isfile(os.path.join(cwd, xyz_file)):
                    subprocess.run(
                        ["cp", xyz_file, temp1_path], stdout=subprocess.PIPE, check=True
                    )
                else:
                    print(f"{xyz_file} not found in {cwd}")
                    sys.exit(1)

    os.chdir(temp1_path)

    # *---------------------------------#
    # * Run the calculation
    if OPERATING_SYTEM in ("win32", "Windows"):
        subprocess.run(
            # ["start", "/b", f"{ORCA_PATH}", input_file, ">", f"{namespace}.out"],
            [f"{ORCA_PATH}", input_file, ">", f"{namespace}.out"],
            stdout=subprocess.PIPE,
            shell=True,
            check=True
        )
    elif OPERATING_SYTEM in ("linux", "Linux", "Darwin"):
        with open(f"{namespace}.out", "w", encoding="utf-8") as out:
            subprocess.run([f"{ORCA_PATH}", input_file], stdout=out, check=True)
    # *---------------------------------#

    print("\n" + 40 * "-")
    print("*" + "ORCA RUN FINISHED!".center(38, " ") + "*")
    print(40 * "-")

    os.chdir("..")
    if OPERATING_SYTEM in ("win32", "Windows"):
        subprocess.run(
            ["copy", f"{temp1_path}\\{namespace}.out", cwd],
            stdout=subprocess.PIPE,
            shell=True,
            check=True
        )
    elif OPERATING_SYTEM in ("linux", "Linux", "Darwin"):
        subprocess.run(
            ["cp", f"{temp1_path}/{namespace}.out", cwd],
            stdout=subprocess.PIPE,
            check=True
        )

    print(40 * "-")
    print("*" + "Output copied to CWD".center(38, " ") + "*")
    print(40 * "-")
