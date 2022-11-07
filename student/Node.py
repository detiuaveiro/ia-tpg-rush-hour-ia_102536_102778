# Authors:
# 102536 Leonardo Almeida
# 102778 Pedro Rodrigues

from student.Functions import *

# car = ( letter, x, y, orientation, length )

class Node:

    def __init__(self, parent, board, cars, action, cost, cursor):
        """
        Node constructor
        """
        self.parent = parent
        self.board = board
        self.cars = cars
        self.action = action
        self.cost = cost
        self.heuristic = self.get_heuristic()
        self.cursor = cursor

        self.vectors =  { 'a': (-1, 0), 'd': (1, 0), 'w': (0, -1), 's': (0, 1) }


    def new_node(self, car, idx, direction, size):
        """
        Create new node
        """
        letter , x , y , orientation, length = car
        # copy the board
        new_board = [*self.board]

        # left 
        if direction == 'a':  
            # change board  
            new_board[y * size + x - 1] = letter
            new_board[y * size + x + length - 1] = 'o'
            # change car
            x -= 1
        # right
        elif direction == 'd':  
            # change board
            new_board[y * size + x + length] = letter
            new_board[y * size + x] = 'o'
            # change car
            x += 1
        # up
        elif direction == 'w': 
            # change board 
            new_board[(y - 1) * size + x] = letter
            new_board[(y + length - 1) * size + x] = 'o'
            # change car
            y -= 1
        # down
        else:  
            # change board
            new_board[(y + length) * size + x] = letter
            new_board[y * size + x] = 'o'
            # change car
            y += 1

        # copy the cars
        new_cars = [*self.cars]
        # change car
        new_car = (letter, x, y, orientation, length)
        new_cars[idx] = new_car
        new_cost, cursor = self.get_cost(car, direction)
        # new_cost = self.cost + self.get_cost2(new_car)
        # create new node
        return Node(self, new_board, new_cars, (letter, direction), new_cost, cursor)


    def expand(self, size):
        """
        Expand node
        """
        # loop through cars
        for idx, car in enumerate(self.cars):
            _, x, y, orientation, length = car
            # horizontal
            if orientation == 'h':
                # move left
                if x > 0 and self.board[y * size + x - 1] == 'o':
                    # create new Node
                    yield self.new_node(car, idx, 'a', size)
                # move right
                if x + length < size and self.board[y * size + x + length] == 'o':
                    # create new Node
                    yield self.new_node(car, idx, 'd', size)
            # vertical
            else:
                # move up
                if y > 0 and self.board[(y - 1) * size + x] == 'o':
                    # create new Node
                    yield self.new_node(car, idx, 'w', size)
                # move down
                if y + length < size and self.board[(y + length) * size + x] == 'o':
                    # create new Node
                    yield self.new_node(car, idx, 's', size)


    def get_cost(self, new_car, direction):
        """
        Cost function
        """
        coords = nearest_coords(self.cursor, new_car)
        cost = self.cost

        # calculate cost
        if self.cursor[0] == coords[0] and self.cursor[1] == coords[1]:
            cost += 1
            if self.parent is None:
                cost += 1
        else:
            cost += 3 + abs(self.cursor[0] - coords[0]) + abs(self.cursor[1] - coords[1])
            if self.parent is None:
                cost -= 1

        # new cursor
        coords[0] += self.vectors[direction][0]
        coords[1] += self.vectors[direction][1]

        return cost, coords


    def get_heuristic(self):
        """
        Heuristic function
        """
        # return 0
        if self.parent is None or self.parent.action is None:
            return 0

        # if self.parent.action[0] == self.action[0]:
        #     return 0
        
        return 0


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
        # return f"{''.join(self.board)}{self.cursor[0]}{self.cursor[1]}"
