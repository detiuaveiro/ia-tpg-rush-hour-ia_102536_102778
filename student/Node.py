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
    # letter : car
    letter_2_car = {}

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

        self.heuristic = self.get_heuristic()


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
        board = self.board

        pos = y * Node.size + x
        if direction == 'a':
            board = f"{board[:pos - 1]}{letter}{board[pos:pos + length - 1]}o{board[pos + length:]}"
            x -= 1
        elif direction == 'd':
            board = f"{board[:pos]}o{board[pos + 1:pos + length]}{letter}{board[pos + length + 1:]}"
            x += 1
        elif direction == 'w':
            board = f"{board[:pos - Node.size]}{letter}{board[pos - Node.size +1:pos + (length-1)*Node.size]}o{board[pos + (length-1)*Node.size + 1:]}"
            y -= 1
        else:
            board = f"{board[:pos]}o{board[pos + 1:pos + length*Node.size]}{letter}{board[pos + length*Node.size + 1:]}"
            y += 1

        new_cars = [*self.cars]
        new_cars[idx] = (letter, x, y, orientation, length)
        action = (letter, direction, idx)
        new_cost, cursor = self.get_cost(car, direction)

        Node.expanded[self.board].append((board, new_cars, action))

        if board not in Node.nodes or Node.nodes[board] >= new_cost:
            Node.nodes[board] = new_cost
            yield Node(self, board, new_cars, action, new_cost, cursor)


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
        if self.action[0] == letter:
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


    def get_heuristic(self):
        """
        Get heuristic
        """
        if Node.size <= 6:
            return 0

        _, x, y, _, length = self.cars[0]
        val = 0
        for pos in range(y * Node.size + x + length, (y+1) * Node.size):
            letter = self.board[pos]
            val += 1
            if letter != 'o':
                _, car_x, car_y, _, car_length = Node.letter_2_car[letter]
                val += 2 + car_length
                car_pos = car_y * Node.size + car_x
                if car_pos - Node.size >= 0 and self.board[car_pos - Node.size] == 'o':
                    val += 1
                elif car_pos + car_length * Node.size < Node.size * Node.size and self.board[car_pos + car_length * Node.size] == 'o':
                    val += 1
                else :
                    val += 2
        return val


    def __lt__(self, other):
        """
        Compare nodes
        """
        return self.cost + self.heuristic < other.cost + other.heuristic