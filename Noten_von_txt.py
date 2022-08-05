import os
import re
import sys

import pandas as pd

# noten_text = r"C:/Scripts/noten.txt"
noten_txt = sys.argv[1]
print(noten_txt)

pattern_ects = r"ECTS:\s(\d+)" #! ECTS
pattern_note = re.compile(r"\bNote:\s(\d\,\d)\s") #! Noten 

with open(noten_txt, "r", encoding="utf-8") as f:
    lines = f.readlines()

marks = []
context = []
ects = []
modul_ects = []

for idx, line in enumerate(lines):
    match_note = re.match(pattern_note, line)
    match_ects = re.search(pattern_ects, line)
    if match_note:
        marks.append(match_note.group(1).replace(",", "."))
        context.append(lines[idx-3].strip())
    elif match_ects:
        ects.append(match_ects.group(1))
        modul_ects.append(line.strip())

# for context, mark in zip(context, marks):
#     print(context, mark)

df = pd.DataFrame({"context": context, "mark": marks})
df2 = pd.DataFrame({"Modul": modul_ects, "ects": ects})
print(df)
print("")
print(df2)
# df2.to_excel("Ects.xlsx")



