import asyncio
# from collections import deque
import heapq
from Functions import *
from Node import Node
from RandomCounter import RandomCounter

# car = ( letter, x, y, orientation, length )


class Agent:

    def __init__(self):
        """
        Agent constructor
        """
        # state
        self.level = None
        self.cursor = None
        self.selected = None
        self.size = None
        self.grid = None
        self.cars = None
        # starting node
        self.root = None
        # path
        self.path = []
        # crazy driver counter
        self.random_counter = RandomCounter(self.path)


    def update(self, state):
        """
        Update the agent
        """

        # New level
        if self.level != state["level"]:
            print(f"New level: {state['level']}")

            self.update_state(state)
            

        # Random move happened
        elif str(self) != state["grid"].split(" ")[1]:
            print("Random move happened")

            # TODO

        
    def update_state(self, state):
        """
        Update agent state
        """
        self.level = state["level"]
        self.cursor = state["cursor"]
        self.selected = state["selected"]
        self.size = state["dimensions"][0]

        board = [*state["grid"].split(" ")[1]]
        self.grid = get_grid(board, self.size)
        self.cars = get_cars(self.grid, self.size)

        self.root = Node(None, board, self.cars, None, 0, 0)

    
    def solve(self):
        """
        Solve the game
        """
        win_pos = self.size - 2
        open_nodes = [self.root]
        heapq.heapify(open_nodes)
        # open_nodes = deque(open_nodes)
        nodes = {str(self.root)}

        while True:
            node = heapq.heappop(open_nodes)
            # node = open_nodes.popleft()

            if test_win(node.cars[0], win_pos):
                print("Solved")
                print(f"Total nodes: {len(nodes)}")
                return get_path(node)

            for new_node in node.expand(self.size):
                new_str = str(new_node)
                if new_str not in nodes:
                    nodes.add(new_str)
                    heapq.heappush(open_nodes, new_node)
                    # open_nodes.append(new_node)

    
    def __str__(self):
        """
        Agent string representation
        """
        return ''.join(''.join(row) for row in self.grid)
    