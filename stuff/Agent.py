import heapq


# car = [ letter, x, y, orientation, length ]
# node = [ parent, grid, cars, action, cost ]

class Agent:

    def __init__(self):
        """
        Agent constructor
        """
        self.cursor = None
        self.selected = None
        self.level = None
        self.size = None
        self.current_grid = None
        self.current_cars = None

        self.root = None

    
    def update_state(self, state):
        """
        Update agent state
        """
        self.cursor = state["cursor"]
        self.selected = state["selected"]

        if self.level is None or self.level != state["level"]:
            self.level = state["level"]
            self.size = state["dimensions"]
            self.current_grid = get_grid(state["grid"].split(" ")[1], self.size)
            self.current_cars = get_cars(self.current_grid, self.size)

            self.root = [None, self.current_grid, self.current_cars, None, 0]


    def solve(self):
        """
        Get best path to solution
        """
        open_nodes = [self.root]
        nodes = [str(self.root[1])]

        while True:
            node = open_nodes.pop(0)

            if test_win(node[1]):
                return get_path(node)

            for new_node in get_new_nodes(node, node[1], node[2], self.size , node[4]):
                if str(new_node[1]) not in nodes:
                    nodes.append(str(new_node[1]))
                    open_nodes.append(new_node)
                    

def get_path(node):
    """
    Get the path to the root node
    """
    if node[0] is None:
        return []
    return get_path(node[0]) + [node[3]]


def test_win(grid):
    """
    Check if the game is won
    """
    return grid[2][5] == 'A'


def get_grid(str, size):
    """
    Get the grid from a string
    """
    return [[*str[i*size[0]:i*size[0]+size[0]]] for i in range(size[1])]


def print_grid(grid):
    """
    Print the grid
    """
    print()
    for i in grid:
        for j in i:
            print(j, end=' ')
        print()
    print()


def get_cars(grid, size):
    """
    Get the cars from grid
    """
    cars = {}
    for y in range(size[1]):
        for x in range(size[0]):
            if grid[y][x] != 'o' and grid[y][x] != 'x':
                if y-1 >= 0 and grid[y-1][x] == grid[y][x]:
                    if grid[y][x] not in cars:
                        cars[grid[y][x]] = [x, y-1, 'v', 2]     # car is vertical
                    else:
                        cars[grid[y][x]][3] += 1                # car length is increased
                elif x-1 >= 0 and grid[y][x-1] == grid[y][x]:
                    if grid[y][x] not in cars:
                        cars[grid[y][x]] = [x-1, y, 'h', 2]     # car is horizontal
                    else:
                        cars[grid[y][x]][3] += 1                # car length is increased
    cars_ = [[i, *cars[i]] for i in cars]
    # cars_.sort(key=lambda x: x[0])
    return cars_


def move_car(car, direction, grid):
    """
    Move the car to a given direction
    """
    match direction:
        case 'a': # left
            grid[car[2]][car[1]-1] = car[0]
            grid[car[2]][car[1]+car[4]-1] = 'o'
            car[1] -= 1
        case 'd': # right
            grid[car[2]][car[1]+car[4]] = car[0]
            grid[car[2]][car[1]] = 'o'
            car[1] += 1
        case 'w': # up
            grid[car[2]-1][car[1]] = car[0]
            grid[car[2]+car[4]-1][car[1]] = 'o'
            car[2] -= 1
        case 's': # down
            grid[car[2]+car[4]][car[1]] = car[0]
            grid[car[2]][car[1]] = 'o'
            car[2] += 1


def get_new_nodes(parent, grid, cars, size, cost):
    """
    Calculate new nodes
    """
    for idx, car in enumerate(cars):
        match car[3]:
            case 'h':   # horizontal

                if car[1] > 0 and grid[car[2]][car[1]-1] == 'o':                    # left

                    new_grid = [i.copy() for i in grid]
                    new_cars = cars.copy()
                    new_cars[idx] = car.copy()
                    move_car(new_cars[idx], 'a', new_grid)
                    yield [parent, new_grid, new_cars, (car[0], 'a'), cost+1]

                if car[1]+car[4] < size[0] and grid[car[2]][car[1]+car[4]] == 'o':  # right

                    new_grid = [i.copy() for i in grid]
                    new_cars = cars.copy()
                    new_cars[idx] = car.copy()
                    move_car(new_cars[idx], 'd', new_grid)
                    yield [parent, new_grid, new_cars, (car[0], 'd'), cost+1]

            case 'v':   # vertical

                if car[2] > 0 and grid[car[2]-1][car[1]] == 'o':                    # up

                    new_grid = [i.copy() for i in grid]
                    new_cars = cars.copy()
                    new_cars[idx] = car.copy()
                    move_car(new_cars[idx], 'w', new_grid)
                    yield [parent, new_grid, new_cars, (car[0], 'w'), cost+1]

                if car[2]+car[4] < size[1] and grid[car[2]+car[4]][car[1]] == 'o':  # down

                    new_grid = [i.copy() for i in grid]
                    new_cars = cars.copy()
                    new_cars[idx] = car.copy()
                    move_car(new_cars[idx], 's', new_grid)
                    yield [parent, new_grid, new_cars, (car[0], 's'), cost+1]