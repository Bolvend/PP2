def count_squared_up_to(n):
    i = 1 
    while i <= n:
        yield i*i
        i += 1
n = int(input("Write integer:"))
for number in count_squared_up_to(n):
    print(number)
