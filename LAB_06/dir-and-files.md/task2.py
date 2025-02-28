import os

path = r'C:\Users\Мухит\Desktop\PP2\LAB_06\мем по физике.jpg'
print("Our path:", path)

print("Does this path exist?", os.access(path, os.F_OK))
print("Can we read it?", os.access(path, os.R_OK))
print("Can we edit it?", os.access(path, os.W_OK))
print("Can we execute it?", os.access(path, os.X_OK))