class Slovo:
    def __init__(self):
        self.enterstr = ""
    def getString(self):
        self.enterstr = input()
    def printString(self):
        print(self.enterstr.upper())

attempt = Slovo()
attempt.getString()
attempt.printString()
