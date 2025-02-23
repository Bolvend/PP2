import re

txt_file = 'lol.txt'

with open(txt_file, 'r') as file:
    lines = file.readlines()


pattern = r"(?=[A-Z])"

for line in lines:
    line = line.strip()
    newline = re.split(pattern, line)
    print (newline)