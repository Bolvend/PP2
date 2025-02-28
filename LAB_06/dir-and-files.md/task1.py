import os

path1 = r'C:\Users\Мухит\Desktop\PP2'
print("Our path:", path1)
content = os.listdir(path1)


print("Its directories:")
for element in content:
    if os.path.isdir(os.path.join(path1, element)):
        print(element)


print("Its elements in general:")
for element in content:
    print(element)

print("Its files:")
for element in content:
    if os.path.isfile(os.path.join(path1, element)):
        print(element)