string = input("Enter a string: ")

uppercase = 0
lowercase = 0

# Loop through each character in the string and count uppercase and lowercase letters
for char in string:
    if char.isupper():
        uppercase += 1
    elif char.islower():
        lowercase += 1

# Print the results
print(f"Number of uppercase letters: {uppercase}")
print(f"Number of lowercase letters: {lowercase}")