#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Author: Martin Dagleish

Version 2.2.1

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

# * Changelog
# * V 2.2.1 - 2022-08-09 
# * - Rewrote the script to make it faster and easiser to understand 
# * - as this was a very old script, which was one of my first coding experiences.
# * V 2.2.0 - 2022-08-09
# * - Move from BA to Scripts folder

import os
import re

import pandas as pd

# ! Variableninitialisierung
user_input = input("Liste an Dateien eingeben (mit .csv und mit , abtrennen):\n")
filename_list = user_input.replace(" ", "").split(",")

filename_list = [
    file if file.endswith(".csv") else file + ".csv" for file in filename_list
]


# TODO:
#* [] Add check if file is already filtered
#* [] if not filtered, run normal version 
#* [] if filtered, run filtered version -> this has to be written

for ind, file in enumerate(filename_list):
    filename = file

    # ! öffnen der .dat / .csv
    df = pd.read_csv(filename, sep=",")  # open csv like files (sep=\t is also possible)
    df = df.dropna(axis=0, how="all")  # * drop if column is empty
    df = df.dropna(axis=1, how="all")  # * drop if row is empty

    #! FILTER for Baseline after rename and delete, because you loose log otherwise
    # * Filter for Baseline
    baseline_drop_namelist = ["Baseline 100%T", "Baseline 0%T"]
    drop_cols_names = [
        col
        for col in df.columns
        if any(col in baseline_name for baseline_name in baseline_drop_namelist)
    ]
    for baseline_col in baseline_drop_namelist:
        df.drop(labels=baseline_col, axis=1, inplace=True, errors="ignore")

    if drop_cols_names:
        print("Baseline columns removed!")
    else:
        print("No baseline to remove!")

    # ! Filter für log -> remove log
    df = df.drop(
        df.iloc[1822:, 0].index, errors="ignore"
    )  # * delete everything after 1823 in CSV (1822 in pandas) -> log removed
    print("Log removed!")

    old_cols = list(df.columns) # zum Aktualiseren der old_cols

    #! Check if first row contains "Wavelength (nm), Abs, …" and delete
    first_row_dict = df.iloc[0].value_counts().to_dict()
    second_row_dict = df.iloc[1].value_counts().to_dict()
    no_wl_first = first_row_dict.get("Wavelength (nm)", 0)
    no_wl_second = second_row_dict.get("Wavelength (nm)", 0)

    if no_wl_first or no_wl_second:  #! test for non-zero value
        if (no_wl_first >= 1):  #! if more than once -> row most-likely contains only wavelength…
            df.drop([0], inplace=True)

        if (no_wl_second >= 1):  #! if more than once -> row most-likely contains only wavelength…
            df.drop([1], inplace=True)

    # * Check if i have to reindex the columns
    # * if not, then the columns are already in the right order (ascending in value)
    if df.iloc[0,0] > df.iloc[1,0]:
        df = df.reindex(index=df.index[::-1])
        df.reset_index(drop=True,inplace=True)  #! reindex df
        print("Columns reindexed!")     

    # Here is the string filters for the column values
    #! list_of_split_lists separated with  _
    new_col_names = []
    overall_time = 0

    for col in df.columns[::2]:
        split_list = col.split("_")
        column_time = str(re.findall("\+?\d+", split_list[-1])[0])
        if "+" in column_time:  # * Inkrement zu 0
            column_time = int(column_time.split("+")[-1])  # * without "+"
            overall_time += column_time
            new_col_names.append(
                str(overall_time)
            )  # * add overall_time after calc to new_col_names
            new_col_names.append("delete")  # * add "delte" str for later
            # ? add value to overall_time and add to list
        elif "+" not in column_time:  # * starting column 0
            # ? set name to 0 in list
            new_col_names.append("0")
            new_col_names.append("delete")  # *  add "delte" str for later

    # ! Renaming and dropping columns accordingly
    df.rename(
        columns={
            old_cols[idx + 1]: new_col_names[idx]
            for idx in range(0, len(new_col_names) - 1)
        },
        inplace=True
    )
    
    df.drop(columns={"delete"}, inplace=True)  # * all deletable columns are removed
    df.rename(columns={df.columns[0]: "Wavelength [nm]"}, inplace=True)  # * rename first column

    # ! Rauschen entfernen
    # df = df.drop(df.iloc[1021:, :].index, errors="ignore")
    # # * delete everything after 1021 in CSV (1021 in pandas) -> noise removed

    # ! Check for file output-type and export accordingly
    filename = os.path.splitext(filename)[0] + "_select.csv"

    df.to_csv("../" + filename, sep=",", index=False)
    print("\n-----------------------------")
    print("EXPORT WAS SUCCESSFUL!")
    print(f"Exported {ind+1}/{len(filename_list)}")
    print("-----------------------------")
