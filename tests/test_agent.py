import asyncio
import time
import sys

sys.path.append('.')

from student.Functions import *
from student.Agent import Agent
from student.Node import Node
from student.KeyGenerator import KeyGenerator

# car = ( letter, x, y, orientation, length )

async def main(level=0, store= False):

    state = {"level": 1, "selected":'', "dimensions": [6, 6], "cursor": [3, 3], "grid": "01 BBCCMxEEELMNAAKLoNooKFFoJGGoooJHHIIo 5"}

    agent = Agent()

    # if store:
    #     k_file = open('tests/key_file.txt', 'w')

    total_times=0
    total_cost = 0
    total_points = 0
    with open("levels.txt") as f:
        for line in f:
            
            if level != 0 and level != int(line.split(" ")[0]):
                continue

            print(f"\nLevel: {line.split(' ')[0]} -> {line.split(' ')[1]}")

            total_points += 2* int(line.split(' ')[2])

            grid_str = line.split(" ")[1]
            size = state["dimensions"][0]
            grid = get_grid(grid_str, size)
            cars = get_cars(grid)

            agent.size = size

            agent.root = Node(None, [*grid_str], cars, None, 0, state["cursor"])

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

                # if store:
                #     k_file.write(key + '\n')
                

                if k_gen.last_key is None:
                    continue
                    
                elif k_gen.moved is not None:
                    path.pop(0)
                    k_gen.moved= None
            

                k_gen.simulate()

            state["cursor"] = k_gen.cursor
 

            print("Real cost: ", cost)
            total_cost += cost
    
    # if store:
    #     k_file.close()

    print("Total Time: ", total_times)
    print("Total Cost: ", total_cost)
    print("Total points: ", total_points)
    print("Max points: ", total_points-total_cost)
    print("Total time to run:" , total_cost/10 /60, "minutes")


if __name__ == "__main__":
    asyncio.run(main())

