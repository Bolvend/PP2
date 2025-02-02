def palindrome(word):
    for i in range(len(word)// 2):
        if word[i] != word[-1 - i]:
            return False
    return True
word = input("Enter string: ")
if palindrome(word):
    print("That is a palindrome")
else:
    print("That is not a palindrome")