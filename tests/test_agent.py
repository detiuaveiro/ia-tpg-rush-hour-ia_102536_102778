import asyncio
import time
import sys

sys.path.append('.')

from student.Functions import *
from student.Agent import Agent
from student.Node import Node
from student.KeyGenerator import KeyGenerator

# car = ( letter, x, y, orientation, length )

async def main(level=0):

    state = {"level": 1, "selected":'', "dimensions": [6, 6], "cursor": [3, 3], "grid": "01 BBCCMxEEELMNAAKLoNooKFFoJGGoooJHHIIo 5"}

    agent = Agent()

    total_times=0
    total_cost = 0
    total_points = 0
    total_moves = 0

    file_path = 'levels.txt'
    # file_path = 'tests/new_levels.txt'
    # file_path = 'tests/levels1000.txt'

    with open(file_path) as f:
        for line in f:
            
            if level != 0 and level != int(line.split(" ")[0]):
                continue

            total_points += 2* int(line.split(' ')[2])

            grid_str = line.split(" ")[1]
            size = int(len(grid_str)**0.5)
            grid = get_grid(grid_str, size)
            cars = get_cars(grid)

            Node.expanded = {}
            Node.size = size
            Node.letter_2_car = {car[0]: car for car in cars}

            agent.path[:] = []
            agent.state_buffer = []
            agent.root = Node(None, grid_str, cars, [None], 0, state["cursor"])
            Node.nodes = {grid_str: 0}

            start = time.time()
            agent.solve()
            end = time.time()

            total_times += end-start
            path = agent.path
            path_len = len(path)

            total_moves += len(path)
            k_gen = KeyGenerator(path)

            cursor = state["cursor"]
            selected = ''
            grid = get_grid(grid_str, size)
            cars = get_cars(grid)
            k_gen.size = size
            k_gen.cursor = cursor
            k_gen.selected = selected
            k_gen.grid = grid
            k_gen.cars = cars

            cost = 0

            while path:
                key = k_gen.next_key()
                cost += 1           
                if k_gen.last_key is None:
                    continue
                elif k_gen.moved is not None:
                    path.pop(0)
                    k_gen.moved= None
                k_gen.simulate()

            state["cursor"] = k_gen.cursor
            total_cost += cost

            # print(f"\nLevel: {line.split(' ')[0]} -> {line.split(' ')[1]}")
            # print("Time: ", end-start)
            # print("Moves: ", path_len)
            # print("Real cost: ", cost)
            

    print("\nTotal Time: ", total_times)
    print("Total Cost: ", total_cost)
    print("Total Moves: ", total_moves)
    print("Total points: ", total_points)
    print("Max points: ", total_points-total_cost)
    print("Total time to run:" , total_cost/10 /60, "minutes")


if __name__ == "__main__":
    asyncio.run(main())

