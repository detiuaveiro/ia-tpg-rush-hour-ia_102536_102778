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
        # pointer to path
        self.path = path
        # moving car
        self.moving = False
        # moved
        self.moved = None


    def update(self, state, new_grid_str):
        """
        Update the key generator
        """
        self.cursor = state["cursor"]
        self.selected = state["selected"]
        self.size = state["dimensions"][0]
        self.grid = get_grid(new_grid_str, self.size)
        self.cars = get_cars(self.grid)
        self.moving = False


    def move_completed(self):
        """
        Move completed
        """
        self.moving = False
        if self.path != []:
            self.path.pop(0)

    
    def check_moved(self):
        """
        Check if the car was moved and update the path
        """
        if self.moving:
            x_, y_, letter = self.moved
            if self.grid[y_][x_] == letter:
                self.move_completed()


    def next_key(self):
        """
        Get keys for a move
        """
        # get the move
        move = self.path[0]
        # get the car
        car, = [car for car in self.cars if car[0] == move[0]] 
        # get the coords to move the cursor to
        coords = nearest_coords(self.cursor, car)

        # move the car
        if self.selected == car[0]:
            return move[1]
        # deselect the car
        if self.selected != '':
            return ' '
        # move cursor left
        if self.cursor[0] > coords[0]:
            return 'a'
        # move cursor right
        if self.cursor[0] < coords[0]:
            return 'd'
        # move cursor up
        if self.cursor[1] > coords[1]:
            return 'w'
        # move cursor down
        if self.cursor[1] < coords[1]:
            return 's'
        # select the car (we are at the right coords)
        if self.selected == '':
            return ' '


    def simulate(self, key):
        """
        Simulate the move of a car
        """

        key_vectors = { 'a': (-1, 0), 'd': (1, 0), 'w': (0, -1), 's': (0, 1) }

        # no car selected
        if self.selected == '':
            # select car
            if key == ' ':
                self.selected = self.grid[self.cursor[1]][self.cursor[0]]
                return
        # car selected
        else:
            # deselect car
            if key == ' ':
                self.selected = ''
                return
            # get the car
            car, = [car for car in self.cars if car[0] == self.selected]
            
            self.moving = True
            letter, x_, y_, _, length = car
            # get coords that changed to letter
            if key_vectors[key][0] == -1:
                x_ -= 1
            elif key_vectors[key][0] == 1:
                x_ += length
            elif key_vectors[key][1] == -1:
                y_ -= 1
            elif key_vectors[key][1] == 1:
                y_ += length
            self.moved = (x_, y_, letter)

            # move car
            move_car(self.grid, car, key)     
            
        # move cursor
        self.cursor[0] += key_vectors[key][0]
        self.cursor[1] += key_vectors[key][1]
                

    def __str__(self):
        """
        String representation of the key generator
        """
        return "".join("".join(row) for row in self.grid)

        