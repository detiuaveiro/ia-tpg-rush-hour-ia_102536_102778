import asyncio
import time

from student.Functions import *
from student.Agent import Agent
from student.Node import Node
from student.KeyGenerator import KeyGenerator

# car = ( letter, x, y, orientation, length )

async def main():

    state = {"level": 1, "selected":'', "dimensions": [6, 6], "cursor": [3, 3], "grid": "01 BBCCMxEEELMNAAKLoNooKFFoJGGoooJHHIIo 5"}

    level = 0

    agent = Agent()

    total_times=0
    total_cost = 0
    with open("levels.txt") as f:
        for line in f:
            
            if level != 0 and level != int(line.split(" ")[0]):
                continue

            print(f"\nLevel: {line.split(' ')[0]} -> {line.split(' ')[1]}")

            grid_str = line.split(" ")[1]
            size = state["dimensions"][0]
            grid = get_grid(grid_str, size)
            cars = get_cars(grid)

            agent.size = size

            agent.root = Node(None, [*grid_str], cars, None, -1, state["cursor"])

            print_grid(grid)

            start = time.time()
            await agent.solve()
            end = time.time()

            total_times += end-start
            path = agent.path

            print("Time: ", end-start)
            # print("Path: ", path)
            print("Moves: ", len(path))
            
            k_gen = KeyGenerator(path)

            cursor = [3,3]
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
                k_gen.simulate(key)
                cost += 1
                if k_gen.moving:
                    k_gen.move_completed()

            print("Real cost: ", cost)
            total_cost += cost


    print("Total Time: ", total_times)
    print("Total Cost: ", total_cost)
    print("Total time to run:" , total_cost/10 /60, "minutes")


if __name__ == "__main__":
    asyncio.run(main())

