import asyncio
from collections import deque
import heapq
from student.Functions import *
from student.Node import Node
from student.RandomCounter import RandomCounter
from student.KeyGenerator import KeyGenerator

# car = ( letter, x, y, orientation, length )

class Agent:

    def __init__(self):
        """
        Agent constructor
        """
        # state
        self.level = None
        self.size = None
        # starting node
        self.root = None
        # path
        self.path = []
        # crazy driver counter
        self.random_counter = RandomCounter(self.path)
        # key generator
        self.key_gen = KeyGenerator(self.path)
        # random moves (grid_str) while calculating the path 
        self.random_moves = []


    def update(self, state):
        """
        Update the agent
        """
        new_grid_str = state["grid"].split(" ")[1]

        # new level
        if self.level is None or self.level != state["level"]:
            print(f"\n\nNew level: {state['level']}\n\n")
            self.new_level(state, new_grid_str)
            return

        grid_str = str(self.key_gen)

        # random move happened
        if new_grid_str != grid_str:
            print("\n\nRandom move happened\n\n")
            self.random_move(state, grid_str, new_grid_str)
            return

        # check if we moved a car
        if self.key_gen.moving:
            # update path
            self.key_gen.move_completed()
            return


    def new_level(self, state, new_grid_str):
        """
        New level
        """
        self.level = state["level"]
        self.size = state["dimensions"][0]
        self.path[:] = []
        self.random_moves = []
        self.key_gen.update(state)

        self.root = Node(None, [*new_grid_str], self.key_gen.cars, None)

        asyncio.create_task(self.solve())


    def random_move(self, state, grid_str, new_grid_str):
        """
        Random move happened
        """
        # add the grid_str to the random moves
        self.random_moves.append(new_grid_str) 

        # check if we are still calculating the path
        if self.path == []:
            return

        while self.random_moves:
            new_grid_str = self.random_moves.pop(0)
            grid_str = str(self.key_gen)

            # if we moved a car at the same time as the random move
            # we need to check if we completed the move
            self.key_gen.check_moved()

            # update the key generator
            self.key_gen.update(state)

            # call the random counter to fix the path
            res = self.random_counter.update_path(grid_str, new_grid_str, self.size)

            # fix didnt work, just in case ...
            if not res:
                print("If i see this print, i will be surprised")
                # re calculate the path
                self.new_level(state, new_grid_str)


    async def solve(self):
        """
        Solve the game
        """
        win_pos = 4
        open_nodes = [self.root]
        # heapq.heapify(open_nodes)
        open_nodes = deque(open_nodes)
        nodes = {str(self.root)}

        while True:

            # await asyncio.sleep(0)

            # node = heapq.heappop(open_nodes)
            node = open_nodes.popleft()

            if test_win(node.cars[0], win_pos):
                print("Solved")
                print(f"Total nodes: {len(nodes)}")
                self.path[:]= get_path(node)
                return

            for new_node in node.expand(self.size):
                new_grid_str= str(new_node)
                if new_grid_str not in nodes:
                    nodes.add(new_grid_str)
                    # heapq.heappush(open_nodes, new_node)
                    open_nodes.append(new_node)


    def action(self):
        """
        Agent action
        """
        # check if we have a path
        if self.path == []:
            return ''

        key = self.key_gen.next_key()
        self.key_gen.simulate(key)
        return key

    
    def __str__(self):
        """
        Agent string representation
        """
        return ''.join(''.join(row) for row in self.grid)
    