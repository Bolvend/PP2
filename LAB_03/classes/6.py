def isNumPrime(x):
    if x < 2:
        return 0
    for i in range(1, x):
        if i != 1 and x%i == 0:
            return 0
    return True
cinlist = input("Enter numbers separated by spaces: ").split()
cinlist = [int(item) for item in cinlist]
prime_numbers = list(filter(lambda x: isNumPrime(x), cinlist))
print("Prime numbers: ")
for x in prime_numbers:
    print (x)