from random import choice
from Node import Node

class Agent:

    def __init__(self):
        """
        Agent constructor
        """
        self.level = None
        self.size = None
        self.cursor = None
        self.start_grid = None
        self.start_cars = None
        self.n_cars = None
        self.root = None


    def update_state(self, state):
        """
        Update the state of the agent
        """
        if self.level is None or self.level != state["level"]:

            self.level = state["level"]
            self.size = state["dimensions"]
            self.cursor = state["cursor"]
            self.start_grid = self.get_grid(state["grid"].split(" ")[1])
            self.start_cars = self.get_cars(self.start_grid)
            self.n_cars = len(self.start_cars)
            
            self.root = Node(self.start_grid, self.start_cars, None)

            # self.solve()


    def get_grid(self, str):
        """
        Get the grid from a string
        """
        return [[*str[i*self.size[0]:i*self.size[0]+self.size[0]]] for i in range(self.size[1])]


    def get_cars(self, grid):
        """
        Get the cars from grid
        """
        cars = {}
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                if grid[y][x] != 'o' and grid[y][x] != 'x':
                    if y-1 >= 0 and grid[y-1][x] == grid[y][x]:
                        if grid[y][x] not in cars:
                            cars[grid[y][x]] = [x, y-1, 0, 2]
                        else:
                            cars[grid[y][x]][3] += 1
                    elif x-1 >= 0 and grid[y][x-1] == grid[y][x]:
                        if grid[y][x] not in cars:
                            cars[grid[y][x]] = [x-1, y, 1, 2]
                        else:
                            cars[grid[y][x]][3] += 1
        cars_ = [[i, *cars[i]] for i in cars]
        cars_.sort(key=lambda x: x[0])
        return cars_

    
    def movable_cars(self, cars, grid):
        """
        Get a list of movable cars and where they can move
        """
        movable=[]
        for i in range(self.n_cars):
            if cars[i][3]: # if car is horizontal
                if cars[i][1]-1 >= 0 and grid[cars[i][2]][cars[i][1]-1] == 'o':
                    movable.append((i, 0)) # 0 = left
                if cars[i][1]+cars[i][4] < self.size[0] and grid[cars[i][2]][cars[i][1]+cars[i][4]] == 'o':
                    movable.append((i, 1)) # 1 = right
            else: # if car is vertical
                if cars[i][2]-1 >= 0 and grid[cars[i][2]-1][cars[i][1]] == 'o':
                    movable.append((i, 2)) # 2 = up
                if cars[i][2]+cars[i][4] < self.size[1] and grid[cars[i][2]+cars[i][4]][cars[i][1]] == 'o':
                    movable.append((i, 3)) # 3 = down
        return movable
        

    def move_car(self, car, direction, grid):
        """
        Move a car in a given direction
        """
        match direction:
            case 0: # left
                grid[car[2]][car[1]-1] = car[0]
                grid[car[2]][car[1]+car[4]-1] = 'o'
                car[1] -= 1
            case 1: # right
                grid[car[2]][car[1]+car[4]] = car[0]
                grid[car[2]][car[1]] = 'o'
                car[1] += 1
            case 2: # up
                grid[car[2]-1][car[1]] = car[0]
                grid[car[2]+car[4]-1][car[1]] = 'o'
                car[2] -= 1
            case 3: # down
                grid[car[2]+car[4]][car[1]] = car[0]
                grid[car[2]][car[1]] = 'o'
                car[2] += 1
  
    def print_grid(self, grid):
        print()
        for i in grid:
            for j in i:
                print(j, end=' ')
            print()
        print()

    def solve(self):
        """
        Find the solution
        """
        open_nodes = [self.root]
        nodes = [self.root.grid_str]
        
        while open_nodes != []:
            node = open_nodes.pop(0)
            
            if self.test_win(node):
                print("Found the solution!")
                return self.get_path(node)
            
            for car_idx, direction in self.movable_cars(node.cars, node.grid):
                new_grid = [row.copy() for row in node.grid]
                new_cars = [car.copy() for car in node.cars]
                
                new_node = Node(new_grid, new_cars, node)
                self.move_car(new_cars[car_idx], direction, new_grid)

                if new_node.grid_str not in nodes:
                    open_nodes.append(new_node)   # pesquisa em largura apenas para teste
                    nodes.append(node.grid_str)
                    
                

    def get_path(self, node:Node):
        """
        Get the path from root to solution
        """
        if node.parent is None:
            return [node]
        
        path = self.get_path(node.parent)
        path += [node]
        return path
    

    def test_win(self, node:Node):
        """
        Check if the player car found the exit for a given node
        """
        # return (node.cars[0][1] + node.cars[0][-1] == self.size[0]-1)
        return node.grid[2][5] == 'A'


    def get_action(self):
        return self.get_random_action()


    def get_random_action(self):
        return choice(["w", "a", "s", "d", " "])



    