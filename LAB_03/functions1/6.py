def rev(slo):
    for x in reversed(slo):
        print (x, end=" ")
    

slo = input("Enter string: ").split()
print("Reversed sentence:")
rev(slo)
