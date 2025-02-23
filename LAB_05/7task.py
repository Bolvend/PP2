import re

txt_file = 'lol.txt'

with open(txt_file, 'r') as file:
    lines = file.readlines()


pattern = r'_([a-z])'

for line in lines:
    line = line.strip()
    newline = re.sub(pattern, lambda match1: match1.group(1).upper(), line)
    print (newline)