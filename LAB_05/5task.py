import re

txt_file = 'lol.txt'

with open(txt_file, 'r') as file:
    lines = file.readlines()

pattern = r"^a.*b$"

matching_lines = []

for line in lines:
    line = line.strip()
    if re.search(pattern, line):
        matching_lines.append(line)

if matching_lines:
    print("Good, I find: " + " ".join(matching_lines))
else:
    print("None")
