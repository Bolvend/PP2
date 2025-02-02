import random

def squidgame():
    print("Hello! What is your name?")
    name = input()
    print("Well,", name + ", I am thinking of a number between 1 and 20.")
    ran = random.randint(1, 20)
    cnt = 0
    while True:
        print("Take a guess.")
        guess = int(input())
        cnt += 1
        if guess == ran:
            break
        elif guess < ran:
            print("Your guess is too low.")
        else:
            print("Your guess is too high.")
    print("Good job, " + name + "! You guessed my number in", cnt, "guesses!")
    return 0

squidgame()
