import os

file_name = r'C:\Users\Мухит\Desktop\PP2\LAB_05\em.txt'
cnt = 0

with open(file_name, 'r') as file:
    for line in file:
        cnt += 1

print("Number of lines:", cnt)
