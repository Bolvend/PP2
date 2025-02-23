import re

txt_file = 'lol.txt'

with open(txt_file, 'r') as file:
    lines = file.readlines()

pattern = r"(?<!^)(?=[A-Z])"  

for line in lines:
    line = line.strip()
    new_line = re.sub(pattern, " ", line)

    if new_line != line:
        print(new_line)
