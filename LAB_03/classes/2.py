class Shape:
    def __init__(self):
        self.area = 0
    def findArea(self):
        return self.area
    
class Square(Shape):
    def __init__(self, length):
        super().__init__()
        self.length = length

    def findArea(self):
        self.area = self.length * self.length
        return self.area


a = int(input("Enter length of a square: "))
sqr = Square(a)
print("Default Area:", sqr.area)
sqr.findArea()
print("New Area:", sqr.area)