def count_twelves(n):
    i = 1 
    while i <= n:
        if i%12 == 0:
            yield i
            i += 1
        else : 
            i += 1
n = int(input("Write integer:"))
for number in count_twelves(n):
    print(number)
