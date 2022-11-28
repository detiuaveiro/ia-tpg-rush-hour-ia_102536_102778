from collections import deque 
import time
import sys 

sys.path.append('.')

def print_grid(grid):
    """
    Print grid
    """
    for i in range(len(grid)):
        for j in range(len(grid)):
            print(grid[i][j], end=' ')
        print()


def get_grid(str_, size):
        """
        Get grid
        """
        # convert board to 2D
        return [[*str_[i:i+size]] for i in range(0, len(str_), size)]


def get_cars(grid):
    """
    Get cars from grid
    """
    size = len(grid)
    # letter : [ x, y, orientation, length ]
    cars = {}
    # loop through grid
    for y in range(size):
        for x in range(size):
            letter = grid[y][x]
            # letter can be a car
            if letter != 'o' and letter != 'x':
                # car is horizontal
                if x + 1 < size and grid[y][x + 1] == letter:
                    # check if car is already in cars
                    if letter not in cars:
                        # add new car
                        cars[letter] = [x, y, 'h', 2]
                    else:
                        # increase car length
                        cars[letter][3] += 1
                # car is vertical
                elif y + 1 < size and grid[y + 1][x] == letter:
                    # check if car is already in cars
                    if letter not in cars:
                        # add new car
                        cars[letter] = [x, y, 'v', 2]
                    else:
                        # increase car length
                        cars[letter][3] += 1

    # convert cars to list and sort by letter
    # [[letter, x, y, orientation, length], ...]
    cars_ = [[i, *cars[i]] for i in cars]
    cars_.sort(key=lambda x: x[0])
    return cars_


def new_node(node, board, cars, car, idx, direction):

    letter , x , y , orientation, length = car

    pos = y * BFS.size + x
    if direction == 'a':
        board = f"{board[:pos - 1]}{letter}{board[pos:pos + length - 1]}o{board[pos + length:]}"
        x -= 1
    elif direction == 'd':
        board = f"{board[:pos]}o{board[pos + 1:pos + length]}{letter}{board[pos + length + 1:]}"
        x += 1
    elif direction == 'w':
        board = f"{board[:pos - BFS.size]}{letter}{board[pos - BFS.size + 1:pos + (length-1)*BFS.size]}o{board[pos + (length-1)*BFS.size + 1:]}"
        y -= 1
    else:
        board = f"{board[:pos]}o{board[pos + 1:pos + length*BFS.size]}{letter}{board[pos + length*BFS.size + 1:]}"
        y += 1

    if board in BFS.states:
        return
    # print(board, direction)
    BFS.states.add(board)

    new_cars = [*cars]
    new_cars[idx] = (letter, x, y, orientation, length)
    yield (node, board, new_cars, (letter, direction))


def expand(node):
 
    _, board, cars, _ = node

    for idx, car in enumerate(cars):
        _, x, y, orientation, length = car
        pos = y * BFS.size + x
        if orientation == 'h':
            if x > 0 and board[pos - 1] == 'o':
                yield from new_node(node, board, cars, car, idx, 'a')
            if x + length < BFS.size and board[pos + length] == 'o':
                yield from new_node(node, board, cars, car, idx, 'd')
        else:
            if y > 0 and board[pos - BFS.size] == 'o':
                yield from new_node(node, board, cars, car, idx, 'w')
            if y + length < BFS.size and board[pos + length*BFS.size] == 'o':
                yield from new_node(node, board, cars, car, idx, 's')

class BFS:

    states = set()
    size = 6

    def __init__(self, state):

        # node = (parent, state, cars, action)
        grid = get_grid(state, BFS.size)
        cars = get_cars(grid)
        self.root = (None, state, cars, None)

        BFS.states= {state}

    
    def get_path(self, node):
        path = []
        while node[0]:
            path.insert(0, node[3])
            node = node[0]
        return path


    def search(self):
        c = 0
        first = 0
        open_nodes = deque([self.root])

        win_pos = BFS.size - 2

        while open_nodes:
            c += 1
            node = open_nodes.popleft()
            if node[2][0][1] == win_pos:
                if first == 0:
                    first = len(self.get_path(node))
                print(first)
                return self.get_path(node)

            for new_node in expand(node):
                open_nodes.append(new_node)

        print(f"{first:3} : {c}")


if __name__ == '__main__':

    level = 0

    total_times=0
    total_cost = 0
    total_points = 0
    with open("levels.txt") as f:
        for line in f:
            
            if level != 0 and level != int(line.split(" ")[0]):
                continue

            # print(f"\nLevel: {line.split(' ')[0]} -> {line.split(' ')[1]}")

            grid_str = line.split(" ")[1]
            BFS.size = int(len(grid_str)**0.5)
            # print_grid(get_grid(grid_str, BFS.size))
            bfs = BFS(grid_str)

            start = time.time()
            path = bfs.search()
            end = time.time()

            total_times += end - start
            # print(f"Time: {end - start}")
            # print("Moves: ", len(path))

        print("\nTotal Time: ", total_times)