#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Author: Martin Dagleish (MRJD)

Version 0.1.0

This script concatenates multiple csvs into one.

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

import argparse
import os
import sys

import pandas as pd

concat_parser = argparse.ArgumentParser(
    prog="concat_csvs.py",
    usage="%(prog)s csv_files [options]",
    description="Concatenate csv files into one csv file. \
        List csv files as arguments (space separated).",
)

concat_parser.add_argument(
    "csv_files", nargs="+", help="list of csv files to concatenate"
)
# concat_parser.add_argument(
#     "-P", 
#     "--path", 
#     metavar="PATH", 
#     help="Choose all csv files in a directory"
# )

concat_parser.add_argument("-o", "--output", help="output file name")


def main():
    args = concat_parser.parse_args()
    # if args.path:
    #     args.csv_files = [
    #         os.path.abspath(f) for f in os.listdir(args.path)
    #     ]
    # else:
    args.csv_files = args.csv_files
    csv_files = [
        os.path.abspath(f)
        for f in args.csv_files
        if os.path.isfile(os.path.abspath(f)) and os.path.abspath(f).endswith(".csv")
    ]
    output = args.output
    if not output:
        output = "concatenated.csv"
    if not os.path.exists(output):
        os.makedirs(os.path.basename(output))
    df = pd.concat((pd.read_csv(f) for f in csv_files))
    df.to_csv(output, sep=",", index=False)
    print("\n-----------------------------")
    print("EXPORT WAS SUCCESSFUL!")
    print(f"Exported {len(csv_files)} files to {output}")
    print("-----------------------------")


if __name__ == "__main__":
    main()
    sys.exit(0)
