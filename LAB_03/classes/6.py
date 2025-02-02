def isNumPrime(x):
    if x < 2:
        return 0
    for i in range(1, x):
        if i != 1 and x%i == 0:
            return 0
    return True
def listOfPrime(cinlist):
    primelist = []
    for x in cinlist:
        if isNumPrime(int(x)):
            primelist.append(x)
    return primelist
cinlist = list(input("Enter numbers separated by spaces: ").split())
prime_numbers = list(filter(lambda x: isNumPrime(x), cinlist))
print("Prime numbers: ")
for x in listOfPrime(cinlist):
    print (x)