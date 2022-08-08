#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: Martin Dagleish

Version 2.1.2

This script filters all .csv files in the current dir, 
that were obtained by using a Agilent Cary 60 UV Vis Spectrometre. 
Those .csv files tend to be very long and result in unnecassary
columns which is why I wrote this script. 

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

#* Changelog 
#* V 2.1.3 - 2022-08-08 
#* - Added argparse for Path or single file input 
#* V 2.1.2 — 2022-08-04
#* - pwd is now working as intended 
#* - export works fine

import os
import sys

try:
    import pandas as pd 
except ImportError:
    print("Pandas is not installed. Please install it using pip install pandas.")
    sys.exit()

try:
    import argparse
except ImportError:
    print("argparse is not installed. Please install it using pip install argparse.")
    sys.exit()


# * Create the parser
spectro_parser = argparse.ArgumentParser(
    prog="general_filter_spectro.py",
    usage="%(prog)s [options]",
    description="Run the general filter script. \
        This script for made for the Agilent Cary 60 UV Vis spectrometre. \
        It converts the output to a more useable format and provides basic filtering.",
)

spectro_parser.add_argument(
    "-P",
    "--path",  #! Positional argument
    metavar="PATH",
    type=str,
    help="The path you want to run the script in. (default: pwd)",
)
spectro_parser.add_argument(
    "-F",
    "--file",  #! Positional argument
    metavar="FILE",
    type=str,
    help="The single file you want to run the script on.",
)


# * Execute the parse_args() method
args = spectro_parser.parse_args()

if not args.path or args.path == ".":
    pwd = os.getcwd()
    # ! Check if export folder exists!
    parent_dir = os.path.dirname(pwd)
    path_filtered_d = os.path.join(parent_dir, "Filtered_Data") 
    if not os.path.isdir(path_filtered_d):
        os.mkdir(path_filtered_d)

    # ! List of local files in current directory
    files = [
        file
        for file in os.listdir(pwd)
        if os.path.isfile(file)
        and (file.endswith(".csv") or file.endswith(".dat"))
        and not (file.endswith("_f_data.csv") or file.endswith("_f_log.csv"))
    ]

if args.file:
    if os.path.isfile(args.file):
        files = [args.file]
    else:
        print("File does not exist. Pls make sure you have the correct path.")
        sys.exit(1)


filter_dict = {
    "OD_": "",
    "0p5_": "",
    "10mm_": "",
    "lex_": "",
    "340nm_": "",
    "illu_": "",
    "10s_": "",
    "210s_": "",
    "90s_": "",
    "10x2mm_": "",
}

def filter_filename(filename_str):
    for old, new in filter_dict.items():
        filename_str = filename_str.replace(old, new)
    return filename_str


file_counter = 0

for file in files:

    # ! open .csv
    df = pd.read_csv(file, sep=",")  # open csv like files (sep=\t is also possible)
    # quick filter
    df = df.dropna(axis=0, how="all")  # * drop if column is empty
    df = df.dropna(axis=1, how="all")  # * drop if row is empty

    # Split log and actual data into two dataframes
    try:
        df_wo_log = df.drop(
            df.iloc[1822:, 0].index
        )  # * delete everything after 1823 in CSV (1822 in pandas) -> log removed
        df_log = df.iloc[1822:, 0]
        print("Data and Log split up successfully!")
    except:
        print("Data and Log could not be split up!")

    #! Check if first row contains "Wavelength (nm), Abs, …" and delete
    first_row_dict = df_wo_log.iloc[0].value_counts().to_dict()
    second_row_dict = df_wo_log.iloc[1].value_counts().to_dict()
    no_wl_first = first_row_dict.get("Wavelength (nm)", 0)
    no_wl_second = second_row_dict.get("Wavelength (nm)", 0)

    if no_wl_first or no_wl_second:  #! test for non-zero value
        if (no_wl_first > 1):  #! if more than once -> row most-likely contains only wavelength…
            df_wo_log.drop([0])

        if (no_wl_second > 1):  #! if more than once -> row most-likely contains only wavelength…
            df_wo_log.drop([1])

    # * Invert columns to start with low values and go up
    df_wo_log = df_wo_log.reindex(index=df_wo_log.index[::-1])  #! invert columns
    df_wo_log.reset_index(inplace=True, drop=True)  #! reindex df

    # * Save col names
    old_cols_names = [col for col in df_wo_log.columns]
    new_cols_names = old_cols_names[:-1]

    # * Change col names for dropping -> "delete" cols
    df_wo_log = df_wo_log.rename(columns={df_wo_log.columns[0]: "Wavelength [nm]"})

    for idx in range(2, len(old_cols_names), 2):
        df_wo_log = df_wo_log.rename(columns={old_cols_names[idx]: "delete"})
    for idx in range(0, len(old_cols_names), 2):
        df_wo_log = df_wo_log.rename(
            columns={old_cols_names[idx + 1]: new_cols_names[idx]}
        )

    # * Delte all cols that are marked as "delete"
    df_wo_log = df_wo_log.drop(columns={"delete"})

    #! FILTER for Baseline after rename and delete, because you loose log otherwise
    # * Filter for Baseline
    try:
        baseline_drop_namelist = ["Baseline 100%T", "Baseline 0%T"]
        drop_cols_names = [
            col
            for col in df_wo_log.columns
            if any(col in baseline_name for baseline_name in baseline_drop_namelist)
        ]
        df_wo_log.drop(labels=drop_cols_names, axis=1, inplace=True)

        if drop_cols_names:
            print("Baseline columns removed!")
        else:
            print("No baseline to remove!")
    except:
        print("Error removing baseline!")

    # ! Remove part of spectrum which only has noise
    df_wo_log = df_wo_log.drop(df_wo_log.iloc[1021:, :].index)

    # ! Check for file output-type and export accordingly
    #! Filename cleanup
    filename = filter_filename(os.path.splitext(file)[0])

    new_filename_data = filename + "_f_data.csv"
    new_filename_log = filename + "_f_log.csv"
    df_wo_log.to_csv(
        os.path.join(path_filtered_d, new_filename_data), sep=",", index=False 
    )  # * for .csv export
    df_log.to_csv(
        os.path.join(path_filtered_d, new_filename_log), sep=",", index=False 
    )  # * for .csv export
    print("------------------------------")
    print("Exporting")
    print(f"    {file}")
    print(f"    as")
    print(f"    {new_filename_data}")
    print("-> EXPORT OF FILE WAS SUCCESSFUL!\n")

    file_counter += 1
    print(f"           {file_counter}/{len(files)} DONE!")
    print("------------------------------\n")

print("\n")
print("--------------------------------")
print("     EXPORT WAS SUCCESSFUL!     ")
print("--------------------------------")
