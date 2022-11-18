# Authors:
# 102536 Leonardo Almeida
# 102778 Pedro Rodrigues

from student.Functions import *

# car = ( letter, x, y, orientation, length )

class KeyGenerator:

    def __init__(self, path):
        """
        KeyGenerator constructor
        """
        # state
        self.cursor = None
        self.selected = None
        self.size = None
        self.grid = None
        self.cars = None
        self.path = path
        self.moved = None
        self.last_key = None


    def update(self, state):
        """
        Update the key generator
        """
        self.cursor = state["cursor"]
        self.selected = state["selected"]
        self.size = state["dimensions"][0]
        self.grid = get_grid(state["grid"].split(" ")[1], self.size)
        self.cars = get_cars(self.grid)
        self.moved = None
        self.last_key = None


    def check_moved(self, state):
        """
        Check if there was a move and if it was successful
        """
        if self.last_key is None:
            return False

        if self.moved is None:
            return True

        new_grid = get_grid(state["grid"].split(" ")[1], self.size)

        if new_grid[self.moved[2]][self.moved[1]] != self.moved[0]:
            self.cursor = state["cursor"]
            self.selected = state["selected"]
            self.moved = None
            return False

        self.path.pop(0)
        self.moved = None
        return True


    def update_moved(self, car, direction):
        """
        Update the moved car
        """
        letter, x, y, _, length = car
        if direction == 'a':
            self.moved = (letter, x - 1, y)
        elif direction == 'd':
            self.moved = (letter, x + length, y)
        elif direction == 'w':
            self.moved = (letter, x, y - 1)
        else:
            self.moved = (letter, x, y + length)

    
    def next_key(self):
        """
        Get keys for a move
        """
        # get the move
        move = self.path[0]
        # get the car
        car, = [car for car in self.cars if car[0] == move[0]]
        coords = nearest_coords(self.cursor, car)

        # move the car
        if self.selected == car[0]:
            self.update_moved(car, move[1])
            self.last_key = move[1]
        # deselect the car
        elif self.selected != '':
            self.last_key = ' '
        # move cursor left
        elif self.cursor[0] > coords[0]:
            self.last_key = 'a'
        # move cursor right
        elif self.cursor[0] < coords[0]:
            self.last_key = 'd'
        # move cursor up
        elif self.cursor[1] > coords[1]:
            self.last_key = 'w'
        # move cursor down
        elif self.cursor[1] < coords[1]:
            self.last_key = 's'
        # select the car (we are at the right coords)
        elif self.selected == '':
            self.last_key = ' '

        return self.last_key

    
    def simulate(self):
        """
        Simulate the move of a car
        """
        key_vectors = { 'a': (-1, 0), 'd': (1, 0), 'w': (0, -1), 's': (0, 1) }

        # no car selected
        if self.selected == '':
            # select car
            if self.last_key == ' ':
                self.selected = self.grid[self.cursor[1]][self.cursor[0]]
                return
        # car selected
        else:
            # deselect car
            if self.last_key == ' ':
                self.selected = ''
                return
            # get the car
            car, = [car for car in self.cars if car[0] == self.selected]
            # move car
            move_car(self.grid, car, self.last_key)     
            
        # move cursor
        self.cursor[0] += key_vectors[self.last_key][0]
        self.cursor[1] += key_vectors[self.last_key][1]
                

    def __str__(self):
        """
        String representation of the key generator
        """
        return "".join("".join(row) for row in self.grid)