# Authors:
# 102536 Leonardo Almeida
# 102778 Pedro Rodrigues

from student.Functions import *

# car = ( letter, x, y, orientation, length )

class Node:

    size = None
    # board : [ (board, cars, action) ... ]
    expanded = {}
    # board : cost
    nodes = {}

    def __init__(self, parent, board, cars, action, cost, cursor):
        """
        Node constructor
        """
        self.parent = parent
        self.board = board
        self.cars = cars
        self.action = action
        self.cost = cost
        self.cursor = cursor


    def expand(self):
        """
        Expand node
        """
        if self.board in Node.expanded:
            for node in Node.expanded[self.board]:
                car = self.cars[node[2][2]]
                new_cost, cursor = self.get_cost(car, node[2][1])
                if node[0] not in Node.nodes or Node.nodes[node[0]] >= new_cost:
                    Node.nodes[node[0]] = new_cost
                    yield Node(self, node[0], node[1], node[2], new_cost, cursor)
        else:
            Node.expanded[self.board] = []
            for idx, car in enumerate(self.cars):
                _, x, y, orientation, length = car
                if orientation == 'h':
                    if x > 0 and self.board[y * Node.size + x - 1] == 'o':
                        yield from self.new_node(car, idx, 'a')
                    if x + length < Node.size and self.board[y * Node.size + x + length] == 'o':
                        yield from self.new_node(car, idx, 'd')
                else:
                    if y > 0 and self.board[(y - 1) * Node.size + x] == 'o':
                        yield from self.new_node(car, idx, 'w')
                    if y + length < Node.size and self.board[(y + length) * Node.size + x] == 'o':
                        yield from self.new_node(car, idx, 's')


    def new_node(self, car, idx, direction):
        """
        Create new node
        """
        letter , x , y , orientation, length = car
        new_board = [*self.board]

        if direction == 'a':    
            new_board[y * Node.size + x - 1] = letter
            new_board[y * Node.size + x + length - 1] = 'o'
            x -= 1
        elif direction == 'd':  
            new_board[y * Node.size + x + length] = letter
            new_board[y * Node.size + x] = 'o'
            x += 1
        elif direction == 'w':  
            new_board[(y - 1) * Node.size + x] = letter
            new_board[(y + length - 1) * Node.size + x] = 'o'
            y -= 1
        else:  
            new_board[(y + length) * Node.size + x] = letter
            new_board[y * Node.size + x] = 'o'
            y += 1

        new_board_str = ''.join(new_board)
        new_cars = [*self.cars]
        new_cars[idx] = (letter, x, y, orientation, length)
        action = (letter, direction, idx)
        new_cost, cursor = self.get_cost(car, direction)

        Node.expanded[self.board].append((new_board_str, new_cars, action))

        if new_board_str not in Node.nodes or Node.nodes[new_board_str] >= new_cost:
            Node.nodes[new_board_str] = new_cost
            # yield Node(self, new_board_str, new_cars, (letter, direction), new_cost, cursor)
            yield Node(self, new_board_str, new_cars, action, new_cost, cursor)


    def get_cost(self, car, direction):
        """
        Get cost
        """
        x, y = self.cursor
        letter, car_x, car_y , orientation, length = car

        if orientation == 'h':
            if x < car_x:
                new_x = car_x
                new_y = car_y
            elif x > car_x + length - 1:
                new_x = car_x + length - 1
                new_y = car_y
            else:
                new_x = x
                new_y = car_y
        else:
            if y < car_y:
                new_x = car_x
                new_y = car_y
            elif y > car_y + length - 1:
                new_x = car_x
                new_y = car_y + length - 1
            else:
                new_x = car_x
                new_y = y

        cost = self.cost
        if self.action[0]== letter:
            cost += 1
        else:
            cost += 3 + abs(new_x - x) + abs(new_y - y)

        if direction == 'a':
            new_x -= 1
        elif direction == 'd':
            new_x += 1
        elif direction == 'w':
            new_y -= 1
        else:
            new_y += 1

        return cost, (new_x, new_y)


    def __lt__(self, other):
        """
        Compare nodes
        """
        return self.cost < other.cost


    def __str__(self):
        """
        Print node
        """
        return f'Board: {self.board}'