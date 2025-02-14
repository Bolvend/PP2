def count_squared_up_to(a , b): 
    while a <= b:
        yield a*a
        a += 1
a = int(input("Write start integer:"))
b = int(input("Write end integer:"))
for number in count_squared_up_to(a , b):
    print(number)
