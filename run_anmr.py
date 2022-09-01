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
anmer_parser = argparse.ArgumentParser(
    prog="run_anmr.py",
    usage="%(prog)s input-file [options]",
    description=f"Run an ANMR calculation for a given input file. -> Script Version {VERSION}",
)

# * Execute the parse_args() method
args = anmer_parser.parse_args()


#! Run the calculation, acutal programm:
if __name__ == "__main__":
    cwd = os.getcwd()

    # * Check if the input files exists
    if not os.path.exists(os.path.join(cwd,"censo_tmp")):
        print("Was the CENSO calculation run? \
              Execute this script from the cwd with the directory containing 'censo_tmp' folder.")
        sys.exit(1)
    
    
    
