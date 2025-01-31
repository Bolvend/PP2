class Shape:
    def __init__(self):
        self.area = 0
    def findArea(self):
        return self.area
    
class Rectangle(Shape):
    def __init__(self, length , width):
        super().__init__()
        self.length = length
        self.width = width
    def findArea(self):
        self.area = self.length * self.width
        return self.area


# Let's test an area method
a = int(input("Enter length of a Rectangle: "))
b = int(input("Enter width of a Rectangle: "))
rect = Rectangle(a , b)
print("Default Area:", rect.area)
rect.findArea()
print("New Area:", rect.area)