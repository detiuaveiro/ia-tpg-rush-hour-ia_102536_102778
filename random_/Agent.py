import asyncio
from Functions import *
import heapq

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

    
    def solve(self):
        """
        Get best path to solution
        """
        open_nodes = [self.root]
        nodes={ get_str(self.root[1])}

        while True:
            # open_nodes.sort(key=lambda x: x[4])
            node = open_nodes.pop(0)

            if test_win(node[1]):
                print(f"Open nodes: {len(open_nodes)}")
                print(f"Nodes: {len(nodes)}")
                
                return get_path(node)

            for new_node in get_new_nodes(node, self.size):
                new_str = get_str(new_node[1])
                if new_str not in nodes:
                    nodes.add(new_str)
                    open_nodes.append(new_node)




    def solve2(self):

        open_nodes= [self.root]
        heapq.heapify(open_nodes)
        nodes= {hash(self.root)}

        while True:
            node = heapq.heappop(open_nodes)

            if test_win(node.grid):
                print(f"Open nodes: {len(open_nodes)}")
                print(f"Nodes: {len(nodes)}")

                return node.get_path()

            for new_node in node.get_children(self.size):
                if hash(new_node) not in nodes:
                    nodes.add(hash(new_node))
                    heapq.heappush(open_nodes, new_node)
