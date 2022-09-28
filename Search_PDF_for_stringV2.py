#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: Martin Dagleish

Version 0.1.0  

This script is a wrapper for the 'pdfgrep' CLI tool for UNIX. 
The original script was written with the PyPDF2 library, which is (of course) a lot 
slower than a CLI-tool which is written in C++ for efficency. 

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

# import os       #* -> os.listdir()
# import PyPDF2   #* reading the PDFs
import json     #* for PPrint of resulting dict 
import pathlib 
import subprocess

# ---------------------------------------------
# TODO: 
# Choice for file: 
# 1. Choose single PDF file
# 2. Choose all local files 
# 3. Pass pattern for filename to pdfgrep 

# Choices for output: 
# 1. Number of hits 
# 2. show results 
# ---------------------------------------------


if __name__ == "__main__":
    while True:
        try: 
            user_file_choice = input("Would you like to search for a single file? (→ 1),\
                all local files (→ 2) \
                or use a pattern match for filenames (→ 3)?")
            if not user_file_choice.isnumeric():       
                raise (Exception("Wrong input!"))
        except TypeError("Enter a valid choice (1,2,3)!"):
            print("")

        file_choice(user_file_choice)
        # try:
        #     user_choice = int(
        #         input(
        #             "Would you like to search for hits (→ '1') or\n just show no. of matches (→ '2')?\n\n"
        #         )
        #     )
        #
        #     user_search_inp = input("What would you like to search for?\n\n")
        #     if user_search_inp.isnumeric():
        #         raise (Exception("Wrong input!"))
        #     break
        # except TypeError("Enter a valid search term! Not a number"):
        #     print("")


    print("--------------")
    print("    RESULT:   ")
    print("--------------")
    print("")

    pdf_files_pwd = [
        pdf for pdf in os.listdir(".") if os.path.isfile(pdf) and pdf.endswith(".pdf")
    ]
    
    if user_choice == 1:
        #! V2:
        result_dict = match_num_w_txt_output(user_search_inp, pdf_files_pwd)

        # * for printing only:
        result_dump = json\
            .dumps(result_dict, indent=2, ensure_ascii=False)\
            .encode("utf8")
        print(result_dump.decode())

    elif user_choice == 2:
        for pdf in pdf_files_pwd:
            print(
                f'The word "{user_search_inp}" was found {num_of_matches(user_search_inp, pdf)} times in {pdf}!'
            )

    print("")
    print("------------------------------")
    print("*          FINSIHED          *")
    print("------------------------------")
