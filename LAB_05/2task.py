import re

txt_file = 'lol.txt'

with open(txt_file, 'r') as file:
    lines = file.readlines()

pattern = r"ab{3,4}"

matching_lines = []

for line in lines:
    line = line.strip()
    if re.fullmatch(pattern, line, re.IGNORECASE):
        matching_lines.append(line)

if matching_lines:
    print("Good, I find: " + " ".join(matching_lines))
else:
    print("None")
