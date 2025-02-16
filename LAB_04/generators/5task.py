def count_squared_down_to(n):
    i = n 
    while i >= 0:
        yield i
        i -= 1
n = int(input("Write integer:"))
for number in count_squared_down_to(n):
    print(number)
