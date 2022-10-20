import time
from Agent import Agent
from Functions import *
import sys

# car = ( letter, x, y, orientation, length )
# node = ( parent, grid, cars, action, cost )

def main():

    sys.setrecursionlimit(1000000)

    state = {"level": 1, "selected":'', "dimensions": [6, 6], "cursor": [3, 3], "grid": "01 BBCCMxEEELMNAAKLoNooKFFoJGGoooJHHIIo 5"}

    level = 0

    agent = Agent()

    total_times=0

    with open("levels.txt") as f:
        for line in f:
            
            if level != 0 and level != int(line.split(" ")[0]):
                continue

            print("\nLevel: ", line.split(" ")[0])

            agent.selected= ''
            agent.cursor = [3, 3]
            agent.level = state["level"]
            agent.size = state["dimensions"]
            agent.current_grid = get_grid(line.split(" ")[1], agent.size)
            agent.current_cars = get_cars(agent.current_grid, agent.size)
            agent.root=(None, agent.current_grid, agent.current_cars, None, 0)


            start = time.time()
            path= agent.solve()
            end = time.time()

            total_times += end-start

            n_keys= 0
            for key in agent.calculate_solution(path):
                agent.simulate(key)
                if agent.current_grid[2][5] == 'A':
                    break
                n_keys += 1

            print("Time: ", end-start)
            # print("Path: ", path)
            print("Moves: ", len(path))
            print("Number of keys: ", n_keys)


    print("Total Time: ", total_times)


if __name__ == "__main__":
    main()