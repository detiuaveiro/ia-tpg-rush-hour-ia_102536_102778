import asyncio
from Functions import *
from Agent import Agent
from Node import Node
import time
from functools import reduce

# car = ( letter, x, y, orientation, length )

async def main():

    state = {"level": 1, "selected":'', "dimensions": [6, 6], "cursor": [3, 3], "grid": "01 BBCCMxEEELMNAAKLoNooKFFoJGGoooJHHIIo 5"}

    level = 0

    agent = Agent()

    total_times=0
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

            agent.root = Node(None, [*grid_str], cars, None)

            print_grid(grid)

            start = time.time()
            path= await agent.solve()
            end = time.time()

            total_times += end-start

            print("Time: ", end-start)
            print("Path: ", path)
            print("Moves: ", len(path))


    print("Total Time: ", total_times)


if __name__ == "__main__":
    asyncio.run(main())

