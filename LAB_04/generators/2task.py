def count_even_up_to(n):
    i = 0 
    while i <= n:
        yield i
        i += 2
n = int(input("Write integer:"))
print(*count_even_up_to(n), sep=" , ")
