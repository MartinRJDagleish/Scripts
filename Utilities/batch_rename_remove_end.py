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

# TODO:
# ? 1. Add file extension to the end of the file name
# ? 2. use "os.walk" to walk through the directories and subdirectories to rename files and directories
# ? 3. use option "topdown=False" for "os.walk" because I need to rename the directories from the bottom up
# ? otherwise I'll create non-existent directories and files

# * -> split name and check if last is exactly 32 characters long if yes then remove it else leave name


def rename_filenames_func(name):
    name, ext = os.path.splitext(name)
    name_splt_lst = name.split(" ")
    if len(name_splt_lst) > 1 and len(name_splt_lst[-1]) == 32:
        name_splt_lst.pop(-1)
    return " ".join(name_splt_lst) + ext


def rename_dirnames_func(name):
    name_splt_lst = name.split(" ")
    if len(name_splt_lst) > 1 and len(name_splt_lst[-1]) == 32:
        name_splt_lst.pop(-1)
    return " ".join(name_splt_lst)


def uniquify(path):
    filename, ext = os.path.splitext(path)
    counter = 1

    while os.path.exists(path):
        path = filename + f"_{counter}" + ext
        counter += 1

    return path


def os_walk_func(path):
    # cwd = path if os.path.isdir(path) else os.path.dirname(path)
    for root, dirs, files in os.walk(cwd, topdown=False):
        # print("Root: " + root)
        # for filename in files:
        #     print("File: " + filename)
        # for dirname in dirs:
        #     print("Dir: " + dirname)
        # * 1. Change filenames
        for filename in files:
            new_filename = rename_filenames_func(filename)
            new_filename = uniquify(os.path.join(root, new_filename))
            os.rename(os.path.join(root, filename), os.path.join(root, new_filename))
            print(f"Renaming {filename} to {new_filename}")
        # * 2. Change dirnames
        for dirname in dirs:
            new_dirname = rename_dirnames_func(dirname)
            new_dirname = uniquify(os.path.join(root, new_dirname))
            os.rename(os.path.join(root, dirname), os.path.join(root, new_dirname))
            print(f"Renaming {dirname} to {new_dirname}")
        # #* 3. Change root -> DO NOT change root -> dirnames will change all of them already
        # new_rootname = rename_dirnames_func(root)
        # os.rename(root, new_rootname)
        # print(root, dirs, files)
        # for dirname in dirs:
        #     for filename in files:
        #         print(os.path.join(dir,file))


if __name__ == "__main__":
    cwd = os.getcwd()
    os_walk_func(cwd)


# *------------------------------------------------------------------------------------------------------------

# def pwd_choice_func():
#     pwd_choice = input("Where do you want to run the script? (. for cwd)")
#     if pwd_choice == ".":
#         pwd = os.getcwd()
#     else:
#         pwd = pwd_choice
#     return pwd


# files = [
#     filename
#     for filename in os.listdir(cwd)
#     if os.path.isfile(os.path.join(cwd, filename))
# ]
# dirs = [
#     dirname
#     for dirname in os.listdir(cwd)
#     if os.path.isdir(os.path.join(cwd, dirname))
# ]

# for filename in files:
#     ext = os.path.splitext(filename)[1]
#     new_filename_lst = filename.split(" ")[:-1]
#     new_filename = " ".join(new_filename_lst) + ext
#     os.rename(os.path.join(cwd, filename), os.path.join(cwd, new_filename))
# for dirname in dirs:
#     new_dirname_lst = dirname.split(" ")[:-1]
#     new_dirname = " ".join(new_dirname_lst)
#     os.rename(os.path.join(cwd, dirname), os.path.join(cwd, new_dirname))
# for filename in files:
#     new_filename_lst = filename.split(" ")[:-1]
#     new_filename = " ".join(new_filename_lst)
#     os.rename(os.path.join(cwd, filename), os.path.join(cwd, new_filename))
# for dirname in dirs:
#     new_dirname_lst = dirname.split(" ")[:-1]
#     new_dirname = " ".join(new_dirname_lst)
#     os.rename(os.path.join(cwd, dirname), os.path.join(cwd, new_dirname))


# if __name__ == "__main__":
#     path = pwd_choice_func()
# while True:
#     files_dir_choice = input("Do you want to rename files or directories? (f/d/fd): ")
#     if files_dir_choice == "f":
#         # -> files function
#         break
#     elif files_dir_choice == "d":
#         # -> dir function
#         break
#     elif files_dir_choice in ("fd","df"):
#         # -> files function and then dir function
#         break
#     else:
#         print("Invalid choice! Try: f/d/fd")
# batch_rename_remove_end(path, files_dir_choice)


# batch_rename_remove_end(path, files_dir_choice)
