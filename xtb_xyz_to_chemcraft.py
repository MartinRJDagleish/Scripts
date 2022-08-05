import os
import re

#! https://regex101.com/r/WivPsO/1
pattern_1 = r"\w+\:\s(-\d+\.\d+)\s\w+\:\s\d\.\d+\s\w+\:\s\d\.\d\.\d\s\(\w+\)"
pattern_2 = r"\b\w\s+((-| )\d[,.]\d+\s+){3,3}"
regex_1 = re.compile(pattern_1)
regex_2 = re.compile(pattern_2)

def main():
    for file in files:
        with open(file, "r", encoding="utf-8") as f:
            lines = f.readlines()
            num_atoms = lines[0]
        with open(os.path.splitext(file)[0] + "_chemcraft.xyz", "w", encoding="utf-8") as f:
            counter = 0
            for line in lines:
                match_2 = re.search(regex_1, line) # search checks anywhere in string, match only checks beginning
                match_3 = re.search(regex_2, line) # https://docs.python.org/3/library/re.html#search-vs-match 
                if num_atoms in line:
                    f.write(line)
                elif match_2: 
                    f.write(match_2.group(1) + "\t frame " + str(counter) + "\txyz file by xtb" + "\n")
                    counter += 1
                elif match_3: 
                    f.write(line)

if __name__ == "__main__":
    choice = input("1) Run on local .xyz files 2) Specified .xyz file: ")
    if choice == "1":
        files = [f for f in os.listdir(".") if os.path.isfile(f) and f.endswith(".xyz")]
        main() 

    elif choice == "2":
        while True:
            filename = input("Enter .xyz file: ")
            if os.path.isfile(filename):
                break
            else:
                print("File not found.")
        files = [filename]
        main()
