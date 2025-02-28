def delay(milliseconds):
    end_time = 1000 * milliseconds 
    start_time = 0 
    while start_time < end_time:
        start_time += 1 
number = float(input("Enter a number: "))
milliseconds = int(input("Enter the delay in milliseconds: "))

delay(milliseconds)

square_root = number ** 0.5
print(f"Square root of {number} after {milliseconds} milliseconds is {square_root}")
