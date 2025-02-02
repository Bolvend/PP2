def allPermutations(current, rem):
    if len(rem) == 0:
        print(current)
    else:
        for x in range(len(rem)):
            new_current = current + rem[x]
            new_remaining = rem[:x] + rem[x+1:]
            allPermutations(new_current, rem)

str = input("Enter string: ")
print("All Permutations:")
allPermutations("", str)
