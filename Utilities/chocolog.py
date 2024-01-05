import re

# import sys
# argv = sys.argv[1:]
# filename = argv[0]

CHOCO_FILE_LOG_PATH = r"C:\ProgramData\chocolatey\logs\chocolatey.log"
filename = CHOCO_FILE_LOG_PATH

# Pattern to match the upgrade section
UPGRADED_PATTERN = (
    r"^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) \d+ \[WARN \] - Upgraded:"
)
END_PROGRAMMES_PATTERN = r"^(\d{4}-\d{2}-\d{2} \d{2}\:\d{2}\:\d{2}\,\d{3}) \d+ \[INFO \] - \n"
# PROGRAMME_LIST_PATTERN = r"^(\d{4}-\d{2}-\d{2} \d{2}\:\d{2}\:\d{2}\,\d{3}) \d+ \[INFO \] -  - (\w+\.*\w+)\s+(v(\d+\.*)+)"
#* NEW regex pattern:
PROGRAMME_LIST_PATTERN = r"^(\d{4}-\d{2}-\d{2} \d{2}\:\d{2}\:\d{2}\,\d{3}) \d+ \[INFO \] -  - (.+)\s+(v(\d+\.*)+)"
re_1 = re.compile(UPGRADED_PATTERN)
re_2 = re.compile(END_PROGRAMMES_PATTERN)
re_3 = re.compile(PROGRAMME_LIST_PATTERN)

# Read the file from the bottom
with open(filename, "r", encoding="ANSI") as f:  # log is saved as ANSI
    lines = f.readlines()

matches_upgrade_line_no = []
end_of_programmes_line_no = []

# 1. Find matches in log and add line_no to list
for line_no, line in enumerate(lines):
    match_1 = re_1.match(line)
    match_2 = re_2.match(line)
    if match_1:
        matches_upgrade_line_no.append(line_no)
    elif match_2:
        end_of_programmes_line_no.append(line_no)

# 2. Find closest line_no after match1 as the "end_of_programmes_line_no"
result_min_ls = [
    min([num for num in end_of_programmes_line_no if num > x], default=None)
    for x in matches_upgrade_line_no
]

# 3. Filter out wrong "matches"
line_no_ranges = [
    (i, j)
    for i, j in zip(matches_upgrade_line_no, result_min_ls)
    if int(j) - int(i) < 20
]

# 4. Filter the lines containing the programme names and version numbers
upgrade_num, end_num = line_no_ranges[-1]
programme_list = lines[upgrade_num:end_num]

# 5. Print out pretty list:
print("***********************************")
print("          CHOCO UPDATE LOG         ")
print("***********************************\n")
print("The following programmes were last updated:")
for programme in programme_list[1:]:
    match = re_3.search(programme)
    programme_name = match.group(2)
    version_no = match.group(3)
    time = match.group(1)
    print(f"    - {programme_name}: {version_no}")


print(f"\nat: {time.split(',')[:-1][0]}")
