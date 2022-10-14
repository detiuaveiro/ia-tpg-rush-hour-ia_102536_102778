class Car:
    def __init__(self, letter, x, y, direction, length):
        self.letter = letter
        self.x = x
        self.y = y
        self.direction = direction
        self.length = length

    def copy(self):
        return Car(self.letter, self.x, self.y, self.direction, self.length)

lst= [1,2,3,4,5]

lst1= [lst[0], lst[1], lst[2], lst[3], lst[4]]