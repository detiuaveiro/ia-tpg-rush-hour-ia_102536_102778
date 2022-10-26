import asyncio
import heapq
from Functions import *

# car = ( letter, x, y, orientation, length )

class Agent:

    def __init__(self):
        """
        Agent constructor
        """
        self.cursor = None
        self.selected = None
        self.level = None
        self.size = None
        
        self.board = None
        self.cars = None

        self.root = None

    
    def solve(self):
        """
        Solve the game
        """
        win_pos = self.size - 2
        open_nodes = [self.root]
        heapq.heapify(open_nodes)
        nodes = {str(self.root)}

        while True:
            node = heapq.heappop(open_nodes)

            if test_win(node, win_pos):
                print("Solved")
                print(f"Total nodes: {len(nodes)}")
                return get_path(node)

            for new_node in node.expand(self.size):
                new_str = str(new_node)
                if new_str not in nodes:
                    nodes.add(new_str)
                    heapq.heappush(open_nodes, new_node)
    