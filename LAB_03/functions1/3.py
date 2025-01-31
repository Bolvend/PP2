def howManyRabbitsAndChickens(numheads, numlegs):
    rabs = int((numlegs - (numheads * 2))/2)
    chks = int(numheads - rabs)
    print("It's", rabs, "rabbits", "and", chks, "chickens")

heads = int(input("Heads: "))
legs = int(input("Legs: "))
howManyRabbitsAndChickens(heads, legs)