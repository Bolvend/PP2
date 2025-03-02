my_list = ["a", "b", "cherry", "d"]

with open("output.txt", "w") as file:
    for item in my_list:
        file.write(item + "\n")

print("List in file output.txt")
