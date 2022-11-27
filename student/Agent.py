# Authors:
# 102536 Leonardo Almeida
# 102778 Pedro Rodrigues

from student.Functions import *
from student.Node import Node
from student.RandomCounter import RandomCounter
from student.KeyGenerator import KeyGenerator

from heapq import heappush, heappop

# car = ( letter, x, y, orientation, length )

class Agent:

    def __init__(self):
        """
        Agent constructor
        """
        self.level = None
        self.root = None
        self.path = []
        self.state_buffer = []
        self.random_counter = RandomCounter(self.path)
        self.key_gen = KeyGenerator(self.path)


    def update(self, state):
        """
        Update the agent
        """
        if self.level is None or self.level != state["level"]:
            self.level = state["level"]
            Node.expanded = {}
            Node.size = state["dimensions"][0]
            self.solve_setup(state)
            return

        if self.key_gen.check_moved(state):
            self.key_gen.simulate()

        self.key_gen.cursor = state["cursor"]
        self.key_gen.selected = state["selected"]

        new_board = state["grid"].split(" ")[1]
        board = str(self.key_gen)
        if new_board != board:
            self.random_move(state)
            return


    def solve_setup(self, state):
        """
        Setup the solve
        """
        self.path[:] = []
        self.state_buffer = []
        self.key_gen.update(state)
        new_board = state["grid"].split(" ")[1]
        self.root = Node(None, new_board, self.key_gen.cars, ['x'], 0, state["cursor"])
        Node.nodes = {new_board: 0}
        self.solve()


    def random_move(self, state):
        """
        Random move
        """
        self.state_buffer.append(state["grid"].split(" ")[1])

        if self.path == []:
            return

        while self.state_buffer != []:  
            new_grid_str = self.state_buffer.pop(0)
            grid_str = str(self.key_gen)

            if new_grid_str == grid_str:
                continue

            self.key_gen.update(state)

            res = self.random_counter.update_path(grid_str, new_grid_str, Node.size)

            if not res:
                self.solve_setup(state)
                return


    def solve(self):
        """
        Solve
        """
        win_pos = Node.size - 2
        open_nodes = [self.root]

        while True:
            node = heappop(open_nodes)

            # if Node.nodes[node.board] != node.cost:
            #     continue

            if test_win(node.cars[0], win_pos):
                self.path[:] = get_path(node)
                return
            for new_node in node.expand():
                heappush(open_nodes, new_node)
            

    def action(self):
        """
        Agent action
        """
        if len(self.path) == 0:
            return ''
        return self.key_gen.next_key()