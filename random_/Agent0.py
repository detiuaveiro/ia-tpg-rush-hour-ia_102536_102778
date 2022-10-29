import asyncio
from random_.Functions0 import *

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


    async def solve(self):
        """
        Get best path to solution
        """
        open_nodes = [self.root]
        nodes = {get_str(self.root[1])}

        while True:
            node = open_nodes.pop(0)

            if test_win(node[1]):
                print("SOLVED")
                self.solution = self.calculate_solution(get_path(node))
                return

            for new_node in get_new_nodes(node, self.size):
                new_str = get_str(new_node[1])
                if new_str not in nodes:
                    nodes.add(new_str)
                    open_nodes.append(new_node)

    
    def solve2(self):
        return []


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













# def update(self, state):
#         """
#         Update the agent
#         """
#         self.cursor = state["cursor"]
#         new_grid_str = state["grid"].split(" ")[1]
#         grid_str = str(self)

#         # new level
#         if self.level != state["level"]:
#             print(f"New level: {state['level']}")

#             self.level = state["level"]
#             self.selected = state["selected"]
#             self.size = state["dimensions"][0]



#             self.grid = get_grid(grid_str, self.size)
#             self.cars = get_cars(self.grid, self.size)

#             # self.root = Node(None, board, self.cars, None, 0, 0)
            
#             self.path[:] = []
#             asyncio.create_task(self.solve())

#         # random move happened
#         elif grid_str != new_grid_str:
#             print("Random move happened")

#             # still calculating the path
#             if self.path == []:
#                 # add the grid_str to the random moves
#                 self.random_moves.append(new_grid_str) 
#                 return

#             # if we moved a car at the same time as the random move
#             # we need to check if we completed the move
#             if self.moved:
#                 x, y, letter = self.moved_car
#                 # car moved successfully
#                 if new_grid_str[y * self.size + x] == 'o':
#                     self.move_completed()

#             # call the random counter to fix the path
#             res = self.random_counter.update_path(grid_str, new_grid_str, self.size)

#             # fix didnt work, just in case ...
#             if not res:
#                 print("If i see this print, i will be surprised")
#                 # calculate a new path
#                 self.path[:] = []
#                 asyncio.create_task(self.solve())
         
#         # car moved successfully
#         elif self.moved:
#             self.move_completed()


#     def move_completed(self):
#         """
#         Move completed
#         """
#         self.moved = False
#         self.moved_car = None
#         self.path.pop(0)
#         # TODO change grid and cars
