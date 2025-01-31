class perevod:
    def __init__(self):
        self.enterTemp = 0
    def getFar(self):
        self.enterTemp = float(input("Enter Fahrenheit temperature: "))
    def printCen(self):
        print(((5 / 9) * (self.enterTemp - 32)))

attempt = perevod()
attempt.getFar()
attempt.printCen()
