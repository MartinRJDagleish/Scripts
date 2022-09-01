#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Author: Martin Dagleish (MRJD)

Version 0.1.0

This is a wrapper script for the ANMR programme. 

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
try:
    import numpy as np
except ImportError:
    print("Please install numpy. Via pip install numpy")
    sys.exit(1)


# * OS running this script
OPERATING_SYTEM = sys.platform

# * Create the parser
anmr_parser = argparse.ArgumentParser(
    prog="run_anmr.py",
    usage="%(prog)s input-file [options]",
    description=f"Run an ANMR calculation for a given input file. -> Script Version {VERSION}",
)
anmr_parser.add_argument(
    "namespace",
    default="anmr",
    help="Add a name for the calculation. This will be used to name the output files. (w/o the .out) %(default)s",
)
anmr_parser.add_argument(
    "--freq",
    type=str,
    default="300",
    help="Choose the lamor frequency for the appriopiate nucleus for the NMR \
        calculation to run. Reasonable: 300 (1H), 162 (31P), ... \
            (default: %(default)s)",
)

# * Execute the parse_args() method
args = anmr_parser.parse_args()

def isfloat(num):
    """
    Helper function for checking if a string is a float.
    """
    try:
        float(num)
        return True
    except ValueError:
        return False

#! Run the calculation, acutal programm:
if __name__ == "__main__":
    cwd = os.getcwd()
    
    namespace = args.namespace.split(".")[0]
        
    freq = args.freq
    if not isfloat(freq):
        print("Please enter a number for the frequency.")
        sys.exit(1)

    # * Check if the input files exists
    if not os.path.exists(os.path.join(cwd,"censo_tmp")):
        print("Was the CENSO calculation run? \
              Execute this script from the cwd with the directory containing 'censo_tmp' folder.")
        sys.exit(1)
    
    os.chdir(os.path.join(cwd,"censo_tmp"))
    
    # * Run the ANMR calculation
    print("Starting the ANMR calculation...")
    print("")
    with open(f"{args.namespace}_anmr.out", "w", encoding="utf-8") as out:
        subprocess.run(
            [
                "anmr",
                "--orca",
                "--plain",
                # plain: coupling constants are read from the CONFXX/NMR/nmrprop.dat written by CENSO
                # instead of the output files of the used QM program package,
                # whose formatting often changes with new versions
                "-mf",  # mf: use the frequenz in MHz
                freq,
                "-mss",  # max spinsystem size
                "12"
            ],
            check=True,
            stdout=out,
        )

    data = np.genfromtxt("anmr.dat")
    THRESHOLD = 0.001
    data2 = data[np.logical_not(data[:, 1] < THRESHOLD)]
    data2 = np.insert(data2, 0, (data[0][0], THRESHOLD), axis=0)
    data2 = np.insert(data2, len(data2), (data[-1][0], THRESHOLD), axis=0)
    np.savetxt(f"{namespace}_anmr.dat", data2, fmt="%2.5e")

    print("\n" + 40 * "-")
    print("*" + "ANMR RUN FINISHED!".center(38, " ") + "*")
    print(40 * "-")

    # * Run ANMR
    print("Starting the NMRplot plotting...")
    print("")

    subprocess.run(
        ["nmrplot.py", "-i", f"{namespace}_anmr.dat", "-o", namespace + "_nmrplot"],
        check=True,
    )
    print("\n" + 40 * "-")
    print("*" + "PLOTTING DONE!".center(38, " ") + "*")
    print(40 * "-")
