#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Author: Martin Dagleish (MRJD)

Version 0.1.0

This script was written for batch processing of RAW photos in a chosen folder.

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

VERSION = "0.1.0"

import pathlib as pl

import imageio
import rawpy

while True:
    user_inp = input("Choose a path to run the script: ('.' for current directory) ")
    if not pl.Path(user_inp).is_dir():
        print("Enter a valid path")
    else:
        path = pl.Path(user_inp)
        break
    
RAWS = [filename.resolve() for filename in path.iterdir() if filename.suffix == ".NEF"]
num_RAWS = len(RAWS)

for idx, RAW in enumerate(RAWS):
    old_filename = RAW.stem
    new_filename = old_filename + "_EDIT.png"
    with rawpy.imread(str(RAW)) as RAW_f:
        rgb = RAW_f.postprocess(
            use_auto_wb=True, dcb_enhance=True
        )  # you can add options at …
    imageio.imsave(new_filename, rgb)
    print(35*"-")
    print("*", f"{idx+1} / {num_RAWS} EXPORTED! ".center(31), "*")
    print(35*"-")

print("")
print("EXPORT FINSIHED!")
print("")