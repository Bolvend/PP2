import math
class Points:
    def __init__(self, x, y):       
        self.x = x
        self.y = y

    def show(self):
        print("Current x coordinate:", self.x)
        print("Current y coordinate:", self.y)

    def move(self, newx, newy):
        self.x = newx
        self.y = newy
    
    def dist(self, coords2):
        dis = math.sqrt((pow((self.x - coords2.x), 2) + pow((self.y - coords2.y), 2)))
        return dis

x1 = int(input("Enter x coordinate: "))
y1 = int(input("Enter y coordinate: "))
coords1 = Points(x1, y1)

coords1.show()
command = input("Enter command move/distance: ")
if command == "move":
    newX = input("Enter a new x coordinate: ")
    newY = input("Enter a new y coordinate: ")
    coords1.move(newX, newY)
    coords1.show()
elif command == "distance":
    newX = int(input("Enter the second point's X coordinate: "))
    newY = int(input("Enter the second point's Y coordinate: "))
    coords2 = Points(newX, newY)
    print("The distance between them:", coords1.dist(coords2))