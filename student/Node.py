from Functions import *
# car = ( letter, x, y, orientation, length )

class Node:

    def __init__(self, parent, board, cars, action, cost, heuristic):
        """
        Node constructor
        """
        self.parent = parent
        self.board = board
        self.cars = cars
        self.action = action
        self.cost = cost
        self.heuristic = heuristic


    def expand(self, size):
        """
        Expand node
        """
        # loop through cars
        for idx, car in enumerate(self.cars):

            letter, x, y, orientation, length = car

            # horizontal
            if orientation == 'h':

                # move left
                if x > 0 and self.board[y * size + x - 1] == 'o':
                    # create new Node
                    new_board = [*self.board]
                    move_car(new_board, car, 'a', size)
                    new_cars = (*self.cars[:idx], (letter, x - 1, y, orientation, length), *self.cars[idx + 1:])
                    yield Node(self, new_board, new_cars, (letter, 'a'), self.cost + 1, 0)
                
                # move right
                if x + length < size and self.board[y * size + x + length] == 'o':
                    # create new Node
                    new_board = [*self.board]
                    move_car(new_board, car, 'd', size)
                    new_cars = (*self.cars[:idx], (letter, x + 1, y, orientation, length), *self.cars[idx + 1:])
                    yield Node(self, new_board, new_cars, (letter, 'd'), self.cost + 1, 0)

            # vertical
            else:

                # move up
                if y > 0 and self.board[(y - 1) * size + x] == 'o':
                    # create new Node
                    new_board = [*self.board]
                    move_car(new_board, car, 'w', size)
                    new_cars = (*self.cars[:idx], (letter, x, y - 1, orientation, length), *self.cars[idx + 1:])
                    yield Node(self, new_board, new_cars, (letter, 'w'), self.cost + 1, 0)

                # move down
                if y + length < size and self.board[(y + length) * size + x] == 'o':
                    # create new Node
                    new_board = [*self.board]
                    move_car(new_board, car, 's', size)
                    new_cars = (*self.cars[:idx], (letter, x, y + 1, orientation, length), *self.cars[idx + 1:])
                    yield Node(self, new_board, new_cars, (letter, 's'), self.cost + 1, 0)


    def __lt__(self, other):
        """
        Compare nodes
        """
        return self.cost + self.heuristic < other.cost + other.heuristic


    def __str__(self):
        """
        String representation of node
        """
        return ''.join(self.board)

