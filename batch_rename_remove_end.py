#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Author: Martin Dagleish

Version 0.1.0

This script is used to batch rename files or dictories in the pwd, which was used 
after Notion exported weird names and I needed better names for Joplin import. 

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
# * V 0.1.0 - 2020-08-18
# * - Initial version

import os

#TODO:
#? 1. Add file extension to the end of the file name
#? 2. use "os.walk" to walk through the directories and subdirectories to rename files and directories
#? 3. 

def batch_rename_remove_end(path, files_dir_chc):
    cwd = path if os.path.isdir(path) else os.path.dirname(path)
    files = [
        filename
        for filename in os.listdir(cwd)
        if os.path.isfile(os.path.join(cwd, filename))
    ]
    dirs = [
        dirname
        for dirname in os.listdir(cwd)
        if os.path.isdir(os.path.join(cwd, dirname))
    ]

    if files_dir_chc == "f":
        for filename in files:
            ext = os.path.splitext(filename)[1]
            new_filename_lst = filename.split(" ")[:-1]
            new_filename = " ".join(new_filename_lst) + ext
            os.rename(os.path.join(cwd, filename), os.path.join(cwd, new_filename))
    elif files_dir_chc == "d":
        for dirname in dirs:
            new_dirname_lst = dirname.split(" ")[:-1]
            new_dirname = " ".join(new_dirname_lst)
            os.rename(os.path.join(cwd, dirname), os.path.join(cwd, new_dirname))
    elif files_dir_chc in ("fd","df"):
        for filename in files:
            new_filename_lst = filename.split(" ")[:-1]
            new_filename = " ".join(new_filename_lst)
            os.rename(os.path.join(cwd, filename), os.path.join(cwd, new_filename))
        for dirname in dirs:
            new_dirname_lst = dirname.split(" ")[:-1]
            new_dirname = " ".join(new_dirname_lst)
            os.rename(os.path.join(cwd, dirname), os.path.join(cwd, new_dirname))
    else:
        print("Invalid choice!")


if __name__ == "__main__":
    pwd_choice = input("Where do you want to run the script? (. for cwd)")
    files_dir_choice = input("Do you want to rename files or directories? (f/d/fd): ")

    if pwd_choice == ".":
        path = os.getcwd()
    else:
        path = pwd_choice

    batch_rename_remove_end(path, files_dir_choice)
