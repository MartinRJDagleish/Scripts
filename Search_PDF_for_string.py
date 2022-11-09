#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: Martin Dagleish

Version 1.1

This script searched through the local PDF text to match any given string. 
You can return the number of hits in a PDF or you can show the context around the hits. 
The latter takes longer (obviously). 


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

import json     #* for PPrint of resulting dict 
import os       #* -> os.listdir()

import PyPDF2   #* reading the PDFs


def match_num_w_txt_output(search_str, pdf_files):
    search_str = search_str.lower()

    result_dict_loc = {}
    for pdf in pdf_files:
        search_word_count = 0
        with open(pdf, "rb") as f:
            result_list = []
            pdfReader = PyPDF2.PdfFileReader(f, strict=False)
            for pageNum in range(pdfReader.numPages):
                pageObj = pdfReader.getPage(pageNum)
                text = pageObj.extractText().encode("utf-8")
                search_text = text.lower().split()
                for idx, string in enumerate(search_text):
                    if search_str in string.decode("utf-8"):
                        search_word_count += 1
                        result = {
                            "Page": pageNum + 1, # +1 because Python counts from 0 
                            "Sentence": " ".join(
                                [
                                    word.decode("utf-8")
                                    for word in search_text[idx - 4 : idx + 5]
                                ]
                            ),  # * 4 words around search
                        }
                        # if any(search_inp in str for ind, str in enumerate(search_text)):
                        #     result = {
                        #         "Page": pageNum,
                        #         "Content": [word for word in search_text[ind-4:ind+4]]
                        #     }
                        result_list.append(result)
            result_list.insert(
                0,
                {
                    "*.*.*.*.": "-------------------------",
                    "  HITS  ": "           "
                    + str(search_word_count)
                    + "             ",
                    ".*.*.*.*": "-------------------------",
                },
            )  # * appending dict after result was created
            result_dict_loc[pdf] = result_list
    return result_dict_loc


#! V1
# def search_with_hits(search_inp, pdf_files_pwd):
#     search_inp = user_search_inp.lower()

#     result_dict = {}
#     for pdf in pdf_files_pwd:
#         with open(pdf, "rb") as f:
#             result_list = []
#             pdfReader = PyPDF2.PdfFileReader(pdf, strict=False)
#             for pageNum in range(pdfReader.numPages):
#                 pageObj = pdfReader.getPage(pageNum)
#                 text = pageObj.extractText().encode("utf-8")
#                 search_text = text.lower().split()
#                 for idx, string in enumerate(search_text):
#                     if search_inp in string.decode("utf-8"):
#                         result = {
#                             "Page": pageNum + 1,
#                             "part. Content": " ".join(
#                                 [
#                                     word.decode("utf-8")
#                                     for word in search_text[idx - 4 : idx + 5]
#                                 ]
#                             ),  # * 4 words around search
#                         }
#                         # if any(search_inp in str for ind, str in enumerate(search_text)):
#                         #     result = {
#                         #         "Page": pageNum,
#                         #         "Content": [word for word in search_text[ind-4:ind+4]]
#                         #     }
#                         result_list.append(result)
#             result_dict[pdf] = result_list  # appending dict after result was created
#     return result_dict


#! V1.1
def num_of_matches(search_inp, pdf_file): #* do not hand whole list of pdfs, but only one pdf at a time 
    search_inp = user_search_inp.lower()

    with open(pdf_file, "rb") as f:
        pdfReader = PyPDF2.PdfFileReader(f, strict=False)
        num_of_matches_int = 0 
        for pageNum in range(pdfReader.numPages):
            pageObj = pdfReader.getPage(pageNum)
            text = pageObj.extractText().encode("utf-8")
            pdf_text = [word.decode("utf-8") for word in text.lower().split()]
            # num_of_matches_int += pdf_text.count(search_inp) # * only matches whole words
            num_of_matches_int += sum(search_inp in string for string in pdf_text) # * matches substrings -> more correct hits 
    return num_of_matches_int 


if __name__ == "__main__":
    while True:
        try:
            user_choice = int(
                input(
                    "Would you like to search for hits (→ '1') or\n just show no. of matches (→ '2')?\n\n"
                )
            )

            user_search_inp = input("What would you like to search for?\n\n")
            if user_search_inp.isnumeric():
                raise (Exception("Wrong input!"))
            break
        except TypeError("Enter a valid search term! Not a number"):
            print("")


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
