import asyncio
# from Functions import *

# car = ( letter, x, y, orientation, length )
# node = ( parent, grid, cars, action, cost )

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

        self.solution = None

        self.task = None


    def update(self, state):
        """
        Update agent state and get best path to solution
        """
        if self.update_state(state):

            if self.task is not None:
                self.task.cancel()

            self.current_grid = get_grid(state["grid"].split(" ")[1], self.size)
            self.current_cars = get_cars(self.current_grid, self.size)
            self.root = (None, self.current_grid, self.current_cars, None, 0)
            self.solution = None            

            self.task = asyncio.create_task(self.solve())


    
    def update_state(self, state):
        """
        Update agent state
        """
        self.cursor = state["cursor"]
        self.selected = state["selected"]

        if self.level is None or self.level != state["level"]:

            # print("\n\n\nNEW LEVEL: ", state["level"], "\n\n\n")

            self.level = state["level"]
            self.size = state["dimensions"]

            return True

        # TODO se o mapa mudar ( houve movimento random )
        if get_str(self.current_grid) != state["grid"].split(" ")[1]:
            
            print("\n\nMOVIMENTO RANDOM")
            print_grid(self.current_grid)
            print_grid(get_grid(state["grid"].split(" ")[1], self.size))

            return True

        return False            
    
    def solve(self):
        """
        Get best path to solution
        """
        open_nodes = [self.root]
        nodes={ get_str(self.root[1])}
        counter=0

        while True:
            counter+=1
            node = open_nodes.pop(0)

            if test_win(node[1]):
                print(f"Counter: {counter}")
                print(f"Nodes: {len(nodes)}")
                return get_path(node)

            for new_node in get_new_nodes(node, self.size):
                new_str = get_str(new_node[1])
                if new_str not in nodes:
                    nodes.add(new_str)
                    open_nodes.append(new_node)



    def calculate_solution(self, path):
        """
        Calculate solution
        """

        print(f"Path: {path}")

        for move in path:
            yield from self.next_actions(move)

    
    def action(self):
        """
        Get next action
        """
        if self.solution is None:
            return ''

        try:
            key = next(self.solution)
            self.simulate(key)
            return key
        except StopIteration:
            return ''


    def next_actions(self, move):
        """
        Get the next keys
        """
        print(self.current_cars)
        car = [car for car in self.current_cars if car[0] == move[0]][0]
        coords= self.nearest_square(car)

        print_grid(self.current_grid)
        print(f"Cursor: {self.cursor}")
        print(f"Selected: {self.selected}")
        print(f"Target car: {car[0]} at {coords}")

        while True:
        
            if self.selected == car[0]:
                yield move[1]           # move the car
                break
            elif self.selected != '':
                yield ' '               # deselect the car
            elif self.cursor[0] > coords[0]:
                yield 'a'               # move cursor left
            elif self.cursor[0] < coords[0]:
                yield 'd'               # move cursor right
            elif self.cursor[1] > coords[1]:
                yield 'w'               # move cursor up
            elif self.cursor[1] < coords[1]:
                yield 's'               # move cursor down
            elif self.selected == '':
                yield ' '               # select the car


    def nearest_square(self, car):
        """
        Nearest car square from cursor
        """
        dists =[]
        for square in range(car[4]):
            match car[3]:
                case 'v':
                    dists.append(dist(self.cursor, (car[1], car[2] + square)))
                case 'h':
                    dists.append(dist(self.cursor, (car[1] + square, car[2])))

        dist_min = min(dists)
        square = dists.index(dist_min)
       
        match car[3]:
            case 'v':    
                return [car[1], car[2]+square]
            case 'h':
                return [car[1]+square, car[2]]
                


    def simulate(self,key):
        """
        Simulate the move of a car
        """

        if self.selected == '':
            match key:
                case 'a':
                    self.cursor[0] -= 1
                case 'd':
                    self.cursor[0] += 1
                case 'w':
                    self.cursor[1] -= 1
                case 's':
                    self.cursor[1] += 1
                case ' ':
                    self.selected = self.current_grid[self.cursor[1]][self.cursor[0]]
        else:
            car = [car for car in self.current_cars if car[0] == self.selected][0]
            match key:
                case 'a':
                    self.cursor[0] -= 1
                    move_car(car, 'a', self.current_grid)
                    car[1] -= 1
                case 'd':
                    self.cursor[0] += 1
                    move_car(car, 'd', self.current_grid)
                    car[1] += 1
                case 'w':
                    self.cursor[1] -= 1
                    move_car(car, 'w', self.current_grid)
                    car[2] -= 1
                case 's':
                    self.cursor[1] += 1
                    move_car(car, 's', self.current_grid)
                    car[2] += 1
                case ' ':
                    self.selected = ''





























from math import dist

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


def get_str(grid):
    """
    Get the string from the grid
    """
    return ''.join([''.join(i) for i in grid])


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
    letter, x, y, _, length = car
    match direction:
        case 'a':                       # left
            grid[y][x-1] = letter
            grid[y][x+length-1] = 'o'
        case 'd':                       # right
            grid[y][x+length] = letter
            grid[y][x] = 'o'
        case 'w':                       # up
            grid[y-1][x] = letter
            grid[y+length-1][x] = 'o'
        case 's':                       # down
            grid[y+length][x] = letter
            grid[y][x] = 'o'


def get_new_nodes(parent, size):
    """
    Calculate new nodes
    """
    grid, cars, cost = parent[1], parent[2], parent[4]
    for idx, car in enumerate(cars):
        letter, x, y, orientation, length = car
        match orientation:
            case 'h':   # horizontal

                if x > 0 and grid[y][x-1] == 'o':                   # move left

                    new_grid = [[*i] for i in grid] # copy the grid
                    move_car(car, 'a', new_grid)
                    new_cars = (*cars[:idx] , (letter, x-1, y, orientation, length) , *cars[idx+1:]) # copy the cars with the change
                    yield (parent, new_grid, new_cars, (letter, 'a'), cost+1)

                if x+length < size[0] and grid[y][x+length] == 'o': # move right

                    new_grid = [[*i] for i in grid] # copy the grid
                    move_car(car, 'd', new_grid)
                    new_cars = (*cars[:idx] , (letter, x+1, y, orientation, length) , *cars[idx+1:]) # copy the cars with the change
                    yield (parent, new_grid, new_cars, (letter, 'd'), cost+1)

            case 'v':   # vertical

                if y > 0 and grid[y-1][x] == 'o':                   # move up

                    new_grid = [[*i] for i in grid] # copy the grid
                    move_car(car, 'w', new_grid)
                    new_cars = (*cars[:idx] , (letter, x, y-1, orientation, length) , *cars[idx+1:]) # copy the cars with the change
                    yield (parent, new_grid, new_cars, (letter, 'w'), cost+1)

                if y+length < size[1] and grid[y+length][x] == 'o': # move down

                    new_grid = [[*i] for i in grid] # copy the grid
                    move_car(car, 's', new_grid)
                    new_cars = (*cars[:idx] , (letter, x, y+1, orientation, length) , *cars[idx+1:]) # copy the cars with the change
                    yield (parent, new_grid, new_cars, (letter, 's'), cost+1)


def heuristic():
    ...
