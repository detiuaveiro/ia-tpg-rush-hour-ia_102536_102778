# Authors:
# 102536 Leonardo Almeida
# 102778 Pedro Rodrigues

from student.Functions import *
from student.Node import Node
from student.RandomCounter import RandomCounter
from student.KeyGenerator import KeyGenerator

import asyncio
from heapq import heapify, heappush, heappop

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
            print(f"\nNew level: {state['level']}\n")
            self.new_level(state, new_grid_str)
            return

        if self.key_gen.check_moved(new_grid_str, state):
            self.key_gen.simulate()

        grid_str = str(self.key_gen)

        # random move happened or grids are not equal
        if new_grid_str != grid_str:
            # print("\nRandom move happened\n")
            self.random_move(state, new_grid_str)
            return


    def new_level(self, state, new_grid_str):
        """
        New level
        """
        self.level = state["level"]
        self.size = state["dimensions"][0]
        self.path[:] = []
        self.random_moves = []
        self.key_gen.update(state, new_grid_str)

        self.root = Node(None, [*new_grid_str], self.key_gen.cars, None, 0, state["cursor"])

        asyncio.create_task(self.solve())


    def random_move(self, state, new_grid_str):
        """
        Random move happened
        """
        # add the grid_str to the random moves
        self.random_moves.append(new_grid_str) 

        # check if we are still calculating the path
        if self.path == []:
            # print("Still calculating the path")
            return

        while self.random_moves != []:
            new_grid_str = self.random_moves.pop(0)
            grid_str = str(self.key_gen)

            if new_grid_str == grid_str:
                continue

            # update the key generator
            self.key_gen.update(state, new_grid_str)

            # call the random counter to fix the path
            res = self.random_counter.update_path(grid_str, new_grid_str, self.size)
            # print(f"Fix worked: {res}")

            # fix didnt work, just in case ... (or on purpose, depends on the random counter)
            if not res:
                print("Fix: recalculate the path")
                # re calculate the path
                self.new_level(state, new_grid_str)
                return


    async def solve(self):
        """
        Solve the game
        """
        win_pos = self.size - 2
        open_nodes = [self.root]
        heapify(open_nodes)
        nodes = {str(self.root): 0}

        while True:

            # await asyncio.sleep(0)

            node = heappop(open_nodes)

            if test_win(node.cars[0], win_pos):
                # print("Solution found")
                # print(f"Cost: {node.cost}")
                # print(f"Open nodes: {len(open_nodes)}")
                self.path[:]= get_path(node)
                return

            for new_node in node.expand(self.size):
                new_grid_str= str(new_node)
                if new_grid_str not in nodes or nodes[new_grid_str] > new_node.cost:
                    nodes[new_grid_str] = new_node.cost
                    heappush(open_nodes, new_node)


    def action(self):
        """
        Agent action
        """
        # check if we have a path
        if self.path == []:
            return ''

        # send the next key
        return self.key_gen.next_key()
    
    